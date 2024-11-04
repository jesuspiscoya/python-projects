import os
from dotenv import load_dotenv
from conexion import Conexion
from mysql.connector import Error

load_dotenv()

host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASS")
database = os.getenv("DB_DATABASE")
host2 = os.getenv("DB_HOST2")
user2 = os.getenv("DB_USER2")
password2 = os.getenv("DB_PASS2")
database2 = os.getenv("DB_DATABASE2")

sp_procedure = 'sp_request_type_sync'

# Conexión a la base de datos
conn = Conexion(host, user, password, database)
conexion = conn.getConexion()

conn2 = Conexion(host2, user2, password2, database2)
conexion2 = conn2.getConexion()

try:
    cursor = conexion.cursor()
    cursor2 = conexion2.cursor()
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
        if sp_procedure in sp_sql:
            print(f"SP '{proc_name}' tiene el SP '{sp_procedure}'")
except Error as e:
    print(f"Error en la base de datos: {e}")
finally:
    cursor.close()
    conn.closeConexion()
