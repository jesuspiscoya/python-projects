import os
import pandas as pd
from dotenv import load_dotenv
from mysql.connector import Error
from conexion import Conexion

load_dotenv()

host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASS")
database = os.getenv("DB_DATABASE")

# Conexión a la base de datos
conn = Conexion(host, user, password, database)
conexion = conn.getConexion()

df = pd.read_excel("mercados.xlsx", sheet_name="CALLAO(C)")

try:
    cursor = conexion.cursor()

    for index, row in df.iterrows():
        valores = (
            row['codigomercado'],
            row['iddistribuidora'],
            row['nombre'],
            str(row['ubigeo']).zfill(6)
        )

        SQL = "UPDATE mercado SET codigomercado = %s WHERE iddistribuidora = %s AND nombre = %s AND ubigeo = %s"
        cursor.execute(SQL, valores)
        print(f"Mercado {row['nombre']} actualizado correctamente")

    conexion.commit()
except Error as e:
    print(f"Error al actualizar: {e}")
finally:
    cursor.close()
    conn.closeConexion()
