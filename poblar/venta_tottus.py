import os
import pandas as pd
import pyodbc
from dotenv import load_dotenv

load_dotenv()

host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASS")
database = os.getenv("DB_DATABASE")

# Cadena de conexión a SQL Server usando pyodbc
conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={
    host};DATABASE={database};Trusted_Connection=yes;'

try:
    df = pd.read_excel(
        "C:/Users/jpiscoya/Downloads/venta_tottus.xlsx", sheet_name="Hoja1")

    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    print("Conexión exitosa a la base de datos.")

    sql = f"INSERT INTO AASS_CuboVentas VALUES ({
        ', '.join(['?'] * len(df.columns))})"

    for index, row in df.iterrows():
        # Insertar datos en la base de datos MySQL
        cursor.execute(sql, tuple(row))
        print(f"{index + 1} filas insertadas correctamente en la tabla")

    # Confirmar los cambios
    conn.commit()
except pyodbc.Error as e:
    print(f"Error al conectar a la base de datos: {e}")
finally:
    # Asegurarse de cerrar la conexión si fue exitosa
    if 'conn' in locals():
        cursor.close()
        conn.close()
        print("Conexión cerrada.")
