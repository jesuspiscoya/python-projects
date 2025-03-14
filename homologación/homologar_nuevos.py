import os
import pandas as pd
from conexion import Conexion
from dotenv import load_dotenv

load_dotenv()

host = os.getenv("DB_HOST")
database = os.getenv("DB_DATABASE")

distributors = [
    "3a",
    "Corseba",
    "Rame",
    "Dinorsa"
]

# Conexión a la base de datos
conn = Conexion(host, database)
conexion = conn.getConexion()

try:
    df = pd.read_excel(
        "homologación/nuevos.xlsx", sheet_name="Hoja1", dtype=str)

    cursor = conexion.cursor()

    for index, row in df.iterrows():
        for distrib in distributors:
            CANAL = "TProvincia" if distrib == "Dinorsa" else "TLima"
            CIUDAD = "Trujillo" if distrib == "Dinorsa" else "Lima"

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
                CANAL,
                CIUDAD,
                distrib,
                f"{row['UNIFLEX']}",
                f"{row['UNIFLEX']}",
                f"{row['SAP']}",
                f"{row['PESO']}",
                f"{distrib}-{CIUDAD}-{row['UNIFLEX']}-{row['UNIFLEX']}",
                f"{distrib}{row['UNIFLEX']}",
                row['ESPROMO'],
                0,
                0
            )

            # Insertar datos en la base de datos
            cursor.execute(SQL, values)

            print(f"[{row['UNIFLEX']}, {distrib}, {
                  CIUDAD}] insertada correctamente.")

    # Confirmar los cambios
    conexion.commit()
except Exception as e:
    print(f"Ha ocurrido un error: {e}")
finally:
    cursor.close()
    conn.closeConexion()
