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
        "homologación/homologar.xlsx", sheet_name="Hoja1", dtype=str)

    cursor = conexion.cursor()

    for index, row in df.iterrows():
        cursor.execute(
            f"SELECT TOP (1) * FROM IN_Producto_PesoFactor where Distribuidora = '{row['DEX']}'")
        peso_factor = cursor.fetchone()

        canal = peso_factor[0]
        ciudad = peso_factor[1]
        distrib = peso_factor[2]
        codigo = row['CODIGO'].strip()

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
            f"{codigo}",
            f"{codigo}",
            f"{row['SAP']}",
            f"{row['PESO']}",
            f"{distrib}-{ciudad}-{codigo}-{codigo}",
            f"{distrib}{codigo}",
            f"{row['ESPROMO']}",
            f"{row['GRAMOS']}",
            f"{row['KILOS']}"
        )

        # Insertar datos en la base de datos
        cursor.execute(SQL, values)
        print(f"[{codigo}, {distrib}, {
              ciudad}] insertada correctamente")

    # Confirmar los cambios
    conexion.commit()
except Exception as e:
    print(f"Ha ocurrido un error: {e}")
finally:
    cursor.close()
    conn.closeConexion()
