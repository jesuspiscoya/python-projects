import os
import string
import secrets
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

CHARS = string.ascii_letters
NUMBERS = string.digits

list_user = []
list_pass = []

try:
    cursor = conexion.cursor()
    # Obtener solo los usuarios que con números
    cursor.execute(r"""
        SELECT UserName FROM User
        WHERE UserName REGEXP '^-?[0-9]+(\.[0-9]+)?$';
    """)
    # cursor.execute("""
    #     SELECT UserName FROM User
    #     WHERE UserName = '70005014';
    # """)
    rows = cursor.fetchall()

    for username, in rows:
        PASSWORD = ''

        # Generar contraseña aleatoria de 6 caracteres
        for _ in range(3):
            PASSWORD += ''.join(secrets.choice(CHARS)) + ''.join(secrets.choice(NUMBERS))
        PASS_UPPER = PASSWORD.upper()
        # PASSWORD = secrets.token_urlsafe(15) + '1Aa'
        # PASSWORD = ''.join(secrets.choice(SECURE_CHARS) for _ in range(15))

        # print(f"Usuario: {username}, Password: {PASS_UPPER}")

        list_user.append(username)
        list_pass.append(PASS_UPPER)

        data = {
            'username': username,
            'password': PASS_UPPER
        }

        response = requests.post(url, json=data, timeout=60)

        if response.status_code == 200:
            print("Respuesta exitosa:", response.json())
        else:
            print(f"Error: {response} {username} {PASS_UPPER}")

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
