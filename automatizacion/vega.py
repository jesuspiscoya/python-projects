import os
import csv
import requests
from datetime import date, timedelta
from dotenv import load_dotenv

load_dotenv()


def generated_csv(url, token, file_name):
    header = {"Authorization": f"Bearer {token}"}
    body = {
        "Proveedor": "6549115da23ca678b53ded25",
        "FechaInicial": str(date.today() - timedelta(days=5)),
        "FechaFinal": str(date.today())
    }

    # Obtener datos de la API
    res = requests.post(url, json=body, headers=header, timeout=120)
    data = res.json()

    if res.status_code == 200:
        values = []

        # Insertar los encabezados
        values.append(list(data[0].keys()))

        # Insertar los valores
        for item in data:
            values.append(list(item.values()))

        # Escribir el archivo CSV con los datos de las Ventas
        with open(rf'\\selloutapp\FTP\Moderno\CORPORACION VEGA\{file_name}.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(values)

        print(f'Se generó el archivo {file_name}.csv con éxito.')
    else:
        print(f"{data.get('message')}")


# Credenciales de acceso
user = os.getenv("USER_VEGA")
psw = os.getenv("PASS_VEGA")

URL = 'http://161.132.213.44/api/loginmdb'
credentials = {'Usuario': user, 'Contraseña': psw}

# Obtener token de Login
response = requests.post(URL, json=credentials, timeout=60)
data = response.json()

if response.status_code == 200:
    token = data.get('token')

    generated_csv('http://161.132.213.44/api/getredis', token, 'VENTAS_VEGA')
    generated_csv(
        'http://161.132.213.44/api/getinventariousuarioconfiltro', token, 'STOCK_VEGA')
else:
    print(f"{data.get('message')}")
