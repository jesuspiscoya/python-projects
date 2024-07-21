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
        SQL = """
        INSERT INTO mercado (iddistribuidora, codigomercado, nombre, ubigeo, estado)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(SQL, tuple(row))
        print(f"Mercado {row['codigomercado']} insertado correctamente")

    conexion.commit()
except Error as e:
    print(f"Error al insertar: {e}")
finally:
    cursor.close()
    conn.closeConexion()
