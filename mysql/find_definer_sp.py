import os
from dotenv import load_dotenv
from conexion import Conexion
from mysql.connector import Error

load_dotenv()

host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASS")
database = os.getenv("DB_DATABASE")

user_procedure = 'gnavarro'

# Conexión a la base de datos
conn = Conexion(host, user, password, database)
conexion = conn.getConexion()

try:
    cursor = conexion.cursor()
    # Obtener los procedimientos almacenados
    cursor.execute(f"""
        SELECT ROUTINE_NAME
        FROM information_schema.ROUTINES
        WHERE ROUTINE_TYPE = 'PROCEDURE'
        AND ROUTINE_SCHEMA = '{database}';
    """)
    rows = cursor.fetchall()

    for (proc_name,) in rows:
        cursor.execute(f"SHOW CREATE PROCEDURE {proc_name}")
        result_row = cursor.fetchone()
        sp_sql = result_row[2]

        # Buscar el DEFINER en el SQL del procedimiento
        if f'DEFINER=`{user_procedure}`@`%`' in sp_sql:
            print(f"SP '{
                  proc_name}' tiene el DEFINER '{user_procedure}'@'%'")
except Error as e:
    print(f"Error en la base de datos: {e}")
finally:
    cursor.close()
    conn.closeConexion()
