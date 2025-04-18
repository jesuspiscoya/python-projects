import os
from datetime import datetime, timezone, timedelta
from conexion import Conexion
from dotenv import load_dotenv
import requests
import pandas as pd

load_dotenv()
tenant_id = os.getenv("TENANT_ID")
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
host = os.getenv("DB_HOST")
database = os.getenv("DB_DATABASE")
EXCEL_PATH = r"\\fileserver\fileserver\Gghh\Correos\ListaCorreos.xlsx"
TEXT_PATH = r"\\fileserver\fileserver\Gghh\Correos\UsuariosNoEncontrados.txt"


def get_token(tenant, client, secret):
    """Obtiene el token de acceso de Azure AD"""

    url_ad = f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token"
    body = {
        "grant_type": "client_credentials",
        "client_id": client,
        "client_secret": secret,
        "scope": "https://graph.microsoft.com/.default"
    }

    response = requests.post(url_ad, data=body, timeout=60)
    data = response.json()
    return data["access_token"]


def get_users(access_token, date):
    """Obtiene los usuarios creados en Azure AD a partir de la fecha especificada"""

    url_graph = f"https://graph.microsoft.com/v1.0/users?$filter=createdDateTime ge {date}&$select=givenName,surname,mailNickname,jobTitle,createdDateTime"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "ConsistencyLevel": "eventual"
    }

    response = requests.get(url_graph, headers=headers, timeout=60)
    data = response.json()

    # Conexión a la base de datos
    conn = Conexion(host, database)
    conexion = conn.getConexion()

    users = []
    sql_dni = """SELECT NOMBRE, APELLIDO_PATERNO, APELLIDO_MATERNO, NRO_DOC_IDENTIDAD
                FROM DATA_MAESTRA
                WHERE NOMBRE COLLATE Latin1_General_CI_AI LIKE ? AND
                APELLIDO_PATERNO + APELLIDO_MATERNO COLLATE Latin1_General_CI_AI LIKE ?"""

    for user in data["value"]:
        if user["givenName"] is not None and user["surname"] is not None and user["jobTitle"] is not None:
            nombre = "%"
            for name in [name.replace('.', '') for name in user["givenName"].split()]:
                nombre += name + "%"

            apellido = "%"
            for last in [last.replace('.', '') for last in user["surname"].split()]:
                apellido += last + "%"

            values = (
                nombre,
                apellido
            )

            try:
                cursor = conexion.cursor()
                cursor.execute(sql_dni, values)

                row = cursor.fetchone()
                if row is not None:
                    users.append({
                        "mail": f"{user['mailNickname']}@laive.pe",
                        "EmailAddress": f"{user['mailNickname']}@laive.pe",
                        "Description": user["jobTitle"],
                        "F4": "",
                        "DNI": row[3],
                        "Telefono": ""
                    })
                else:
                    user_not_found({
                        "name": user["givenName"],
                        "lastname": user["surname"],
                        "mail": f"{user['mailNickname']}@laive.pe"
                    })
            except Exception as e:
                print(f"Ha ocurrido un error: {e}")
            finally:
                cursor.close()

    conn.closeConexion()
    return users


def insert_user(user):
    """Inserta un usuario en un archivo Excel"""

    df = pd.read_excel(EXCEL_PATH)
    df = df._append(user, ignore_index=True)
    df.to_excel(EXCEL_PATH, index=False)

    print(f"Usuario insertado: {user["mail"]}.")


def user_not_found(user):
    """Inserta los usuarios no encontrados en un archivo de texto"""

    # Abrir el archivo en modo de agregar (esto no sobrescribe, solo agrega al final)
    with open(TEXT_PATH, "a", encoding="utf-8") as archivo:
        archivo.write(f"\n{user["name"]} {user["lastname"]} - {user["mail"]}.")

    print(f"Usuario no encontrado: {user["name"]} {user["lastname"]}")


token = get_token(tenant_id, client_id, client_secret)
yesterday = datetime.now(timezone.utc) - timedelta(days=1)
date_utc = yesterday.strftime("%Y-%m-%dT%H:%M:%SZ")

for user_ad in get_users(token, date_utc):
    insert_user(user_ad)
