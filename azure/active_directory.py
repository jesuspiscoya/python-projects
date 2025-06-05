import os
from datetime import datetime, timezone, timedelta
from conexion import Conexion
from dotenv import load_dotenv
import requests

load_dotenv()
tenant_id = os.getenv("TENANT_ID")
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
host = os.getenv("DB_HOST")
database = os.getenv("DB_DATABASE")


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

    users = []
    # url_graph = f"https://graph.microsoft.com/v1.0/users?$filter=createdDateTime ge {date}&$select=givenName,surname,mailNickname,jobTitle,faxNumber,createdDateTime"
    url_graph = "https://graph.microsoft.com/v1.0/users?$select=givenName,surname,mailNickname,jobTitle,faxNumber,mobilePhone,createdDateTime&$top=999"
    headers = {"Authorization": f"Bearer {access_token}"}

    while url_graph:
        response = requests.get(url_graph, headers=headers, timeout=60)
        data = response.json()

        url_graph = data["@odata.nextLink"] if "@odata.nextLink" in data else None

        for user in data["value"]:
            if user["faxNumber"] is not None and user["faxNumber"].isdigit():
                users.append((
                    f"{user['mailNickname']}@laive.pe",
                    f"{user['mailNickname']}@laive.pe",
                    user["jobTitle"],
                    "",
                    user['faxNumber'],
                    user['mobilePhone'],
                    datetime.now()
                ))

    return users


def insert_user(users):
    """Inserta los usuarios a la base de datos"""

    conn = Conexion(host, database)
    conexion = conn.getConexion()
    sql_user = "INSERT INTO listacorreos_prueba VALUES (?, ?, ?, ?, ?, ?, ?)"

    try:
        cursor = conexion.cursor()
        cursor.executemany(sql_user, users)
        conexion.commit()

        print(f"{len(users)} usuarios insertados correctamente.")
    except Exception as e:
        print(f"Ha ocurrido un error: {e}")
    finally:
        cursor.close()


token = get_token(tenant_id, client_id, client_secret)
yesterday = datetime.now(timezone.utc) - timedelta(days=10)
date_utc = yesterday.strftime("%Y-%m-%dT%H:%M:%SZ")

ad_users = get_users(token, date_utc)
insert_user(ad_users)
