import os
import pandas as pd
from dotenv import load_dotenv
from conexion import Conexion
from mysql.connector import Error

load_dotenv()

host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASS")
database = os.getenv("DB_DATABASE")

# Conexión a la base de datos
conn = Conexion(host, user, password, database)
conexion = conn.getConexion()

# Cargar datos desde Excel
df_factura = pd.read_excel("factura.xlsx", sheet_name="Factura")
df_detalle = pd.read_excel("factura.xlsx", sheet_name="Factura Detalle")

# Insertar datos en la base de datos MySQL
try:
    cursor = conexion.cursor()

    # Iterar sobre cada fila del DataFrame y ejecutar una inserción
    for index, row_factura in df_factura.iterrows():
        factura = (
            row_factura['iddistribuidora'],
            row_factura['numerofactura'],
            str(row_factura['codigovendedor']).zfill(3),
            row_factura['codigocliente'],
            str(row_factura['codigozona']).zfill(4),
            row_factura['abreviacion'],
            str(row_factura['codigoalmacen']).zfill(2),
            row_factura['credito'],
            row_factura['monto'],
            row_factura['fechafactura'],
            row_factura['fechaultimopago'],
            row_factura['pagado'],
            row_factura['anulado'],
            row_factura['estado']
        )

        SQL_FACTURA = """INSERT INTO factura (
            iddistribuidora,
            numerofactura,
            codigovendedor,
            codigocliente,
            codigozona,
            abreviacion,
            codigoalmacen,
            credito,
            monto,
            fechafactura,
            fechaultimopago,
            pagado,
            anulado,
            estado)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(SQL_FACTURA, factura)
        id_factura = cursor.lastrowid

        for index, row_detalle in df_detalle.iterrows():
            if row_detalle['numerofactura'] == row_factura['numerofactura']:
                detalle = (
                    row_detalle['iddistribuidora'],
                    id_factura,
                    row_detalle['numerofactura'],
                    str(row_detalle['codigoproducto']).zfill(4),
                    row_detalle['cantidad'],
                    row_detalle['precio'],
                    row_detalle['estado'],
                    row_detalle['entregado']
                )

                SQL_DETALLE = """INSERT INTO facturadetalle (
                    iddistribuidora,
                    idfactura,
                    numerofactura,
                    codigoproducto,
                    cantidad,
                    precio,
                    estado,
                    entregado,
                    bonificacion)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,0)"""
                cursor.execute(SQL_DETALLE, detalle)

                # Confirmar la transacción
                conexion.commit()
                print(
                    f"{cursor.rowcount} filas insertadas correctamente en la tabla")
except Error as e:
    print(f"Error al insertar datos en MySQL: {e}")
finally:
    cursor.close()
    conn.closeConexion()
