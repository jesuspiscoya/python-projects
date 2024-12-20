import os
import pandas as pd
from conexion import Conexion
from dotenv import load_dotenv

load_dotenv()

host = os.getenv("DB_HOST")
database = os.getenv("DB_DATABASE")

# Conexión a la base de datos
conn = Conexion(host, database)
conexion = conn.getConexion()

try:
    df = pd.read_excel(
        "homologación/productos.xlsx", sheet_name="Hoja1", dtype=str)

    cursor = conexion.cursor()

    for index, row in df.iterrows():
        cursor.execute(
            f"SELECT TOP (1) * FROM IN_Producto_PesoFactor where Distribuidora = '{row['DEX']}'")
        peso_factor = cursor.fetchone()

        canal = peso_factor[0]
        ciudad = peso_factor[1]
        distrib = peso_factor[2]

        SQL = """INSERT INTO IN_Producto_PesoFactor (
                Canal,
                Ciudad,
                Distribuidora,
                CodigoProductoDT,
                CodigoProducto,
                CodigoSAP,
                PesoFactor,
                Llave,
                PK,
                Promocion,
                Gramos,
                Kilos)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"""

        values = (
            canal,
            ciudad,
            distrib,
            f"{row['CODIGO']}",
            f"{row['CODIGO']}",
            f"{row['SAP']}",
            f"{row['PESO']}",
            f"{distrib}-{ciudad}-{row['CODIGO']}-{row['CODIGO']}",
            f"{distrib}{row['CODIGO']}",
            0,
            0,
            0
        )

        # Insertar datos en la base de datos MySQL
        cursor.execute(SQL, values)
        print(
            f"[{row['CODIGO']}, {distrib}, {ciudad}] insertada correctamente en la tabla")

    # Confirmar los cambios
    conexion.commit()
except Exception as e:
    print(f"Ha ocurrido un error: {e}")
finally:
    cursor.close()
    conn.closeConexion()
