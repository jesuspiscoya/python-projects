import json
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

# Cargar datos desde Excel
df = pd.read_excel("vendedores.xlsx", sheet_name="Daloz")

df_claves = df.copy()

nuevas_claves = []

try:
    cursor = conexion.cursor()

    for index, row in df.iterrows():
        codigo = str(row['Codigo Usuario']).zfill(3)
        SQL = f"""SELECT * FROM logmobile WHERE origen='login'
        AND iddistribuidora='6' AND codigovendedor='{codigo}'
        ORDER BY 1 DESC LIMIT 20"""
        cursor.execute(SQL)
        rows = cursor.fetchall()

        if len(rows) == 0:
            nuevas_claves.append("")
            print(f"No se encontraron datos para el vendedor {codigo}")
        else:
            nuevas_claves.append("")
            for row in rows:
                if row[5] == "Exito":
                    diccionario = json.loads(row[7])
                    nuevas_claves[len(nuevas_claves) - 1] = diccionario['pass']
                    break

            if nuevas_claves[len(nuevas_claves) - 1] == "":
                print(f"No se encontraron datos para el vendedor {codigo}")

except Error as e:
    print(f"Error al consultar datos en MySQL: {e}")
finally:
    cursor.close()
    conn.closeConexion()

df_claves['Clave'] = nuevas_claves
df_claves.to_excel("claves.xlsx", index=False)
