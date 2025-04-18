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
        "homologación/padrehijo.xlsx", sheet_name="Hoja1", dtype=str)

    cursor = conexion.cursor()

    SQL_INSERT = "INSERT INTO ProductoPadreHijo VALUES (?,?,?,?)"
    SQL_UPDATE = """UPDATE ProductoPadreHijo
                SET CodigoAntiguo=?, CodigoSAPVigente=?
                WHERE CodigoSAP=?"""

    for index, row in df.iterrows():
        if pd.isna(row['ANTIGUO']):
            values = (
                f"{row['SAP']}",
                f"{row['MATERIAL']}",
                "",
                f"{row['VIGENTE']}"
            )

            # Insertar datos en la base de datos
            cursor.execute(SQL_INSERT, values)
            print(f"El código {row['SAP']} se insertó correctamente.")
        else:
            values = (
                f"{row['ANTIGUO']}",
                f"{row['VIGENTE']}",
                f"{row['SAP']}"
            )

            # Actualiza datos en la base de datos
            cursor.execute(SQL_UPDATE, values)
            print(f"El código {row['SAP']} se actualizó con {row['VIGENTE']}.")

    # Confirmar los cambios
    conexion.commit()
except Exception as e:
    print(f"Ha ocurrido un error: {e}")
finally:
    # cursor.close()
    conn.closeConexion()
