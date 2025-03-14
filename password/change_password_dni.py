import os
import pandas as pd
import requests
from dotenv import load_dotenv
from mysql.connector import Error
from conexion import Conexion

load_dotenv()

host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASS")
database = os.getenv("DB_DATABASE")

url = os.getenv("URL_API")
path_excel = os.getenv("PATH_EXCEL")

# Conexión a la base de datos
conn = Conexion(host, user, password, database)
conexion = conn.getConexion()

list_user = []
list_pass = []

try:
    cursor = conexion.cursor()
    # Obtener solo los usuarios que con números
    cursor.execute(r"""
        SELECT DocumentNumber FROM User
        WHERE UserName NOT LIKE '%@%';
    """)
    # cursor.execute("""
    #     SELECT UserName FROM User
    #     WHERE UserName = '70005014';
    # """)
    rows = cursor.fetchall()

    for document, in rows:
        print(f"Usuario: {document}, Password: {document}")

        list_user.append(document)
        list_pass.append(document)

        data = {
            'username': document,
            'password': document
        }

        response = requests.post(url, json=data, timeout=60)

        if response.status_code == 200:
            print("Respuesta exitosa:", response.json())
        else:
            print(f"Error: {response} {document} {document}")

    df = pd.DataFrame({
        'USUARIOS': list_user,
        'CONTRASEÑAS': list_pass
    })

    # Crear un archivo Excel
    df.to_excel('usuarios.xlsx', index=False, engine='openpyxl')

    print("Archivo Excel creado con éxito.")
except Error as e:
    print(f"Error en la base de datos: {e}")
finally:
    cursor.close()
    conn.closeConexion()
