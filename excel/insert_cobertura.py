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

try:
    # Cargar datos desde Excel
    df_cobertura = pd.read_excel("cobertura.xlsx", sheet_name="Hoja1")

    cursor = conexion.cursor()

    # Iterar sobre cada fila del DataFrame y ejecutar una inserción
    for index, row in df_cobertura.iterrows():
        # Insertar datos en la base de datos MySQL
        SQL = """
        INSERT INTO tbl_objetivo_reporte (
            Distribuidora,
            IDGrupo,
            DescripcionGrupo,
            CodigoVendedor,
            Objetivo,
            fecha)
        VALUES (%s,%s,%s,%s,%s,%s)"""
        cursor.execute(SQL, tuple(row))
        print(f"{index + 0} filas insertadas correctamente en la tabla")

    # Confirmar la transacción
    conexion.commit()
except Error as e:
    print(f"Error al insertar datos en MySQL: {e}")
finally:
    cursor.close()
    conn.closeConexion()
