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

# Conexión a la base de datos
conn = Conexion(host, user, password, database)
conexion = conn.getConexion()

conn2 = Conexion(host2, user2, password2, database2)
conexion2 = conn2.getConexion()

tables_list = [
    'ProcessLogs',
    'Request',
    'RequestApplication',
    'RequestChannel',
    'RequestDetail',
    'RequestReason',
    'RequestState',
    'RequestType',
    '__EFMigrationsHistory',
]


def get_table_ddl(cursor_1, cursor_2, table_name):
    try:
        cursor_1.execute(f"SHOW CREATE TABLE {table_name}")
        ddl1 = cursor_1.fetchone()[1]

        cursor_2.execute(f"SHOW CREATE TABLE {table_name}")
        ddl2 = cursor_2.fetchone()[1]

        if ddl1 == ddl2:
            print(f"LAS TABLAS {table_name} SON IGUALES.")
            return True
        else:
            return False
    except:
        print(f"La tabla {table_name} no existe.")
        return None


def get_column_describe(cursor_1, cursor_2, table_name):
    try:
        cursor_1.execute(f"DESCRIBE {table_name}")
        column1 = cursor_1.fetchall()
        column1.sort(key=lambda x: x[0])

        cursor_2.execute(f"DESCRIBE {table_name}")
        column2 = cursor_2.fetchall()
        column2.sort(key=lambda x: x[0])

        if column1 == column2:
            return True
        else:
            return False
    except Error as error:
        print(f"Ocurrió un error en las columnas: {error}")
        return None


def get_constraint(cursor_1, cursor_2, table_name):
    try:
        cursor_1.execute(f"""
            SELECT CONSTRAINT_NAME,COLUMN_NAME,REFERENCED_TABLE_NAME,REFERENCED_COLUMN_NAME
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE TABLE_NAME = '{table_name}' AND TABLE_SCHEMA = '{database}';
        """)
        constraint1 = cursor_1.fetchall()

        cursor_2.execute(f"""
            SELECT CONSTRAINT_NAME,COLUMN_NAME,REFERENCED_TABLE_NAME,REFERENCED_COLUMN_NAME
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE TABLE_NAME = '{table_name}' AND TABLE_SCHEMA = '{database2}';
        """)
        constraint2 = cursor_2.fetchall()

        if constraint1 == constraint2:
            return True
        else:
            return False
    except Error as error:
        print(f"Ocurrió un error en la BD: {error}")
        return None


try:
    cursor = conexion.cursor()
    cursor2 = conexion2.cursor()

    for t_name in tables_list:
        tables = get_table_ddl(cursor, cursor2, t_name)

        if tables is None or tables is True:
            continue

        columns = get_column_describe(cursor, cursor2, t_name)
        constraints = get_constraint(cursor, cursor2, t_name)

        if columns:
            print(f"LAS TABLAS {t_name} SON IGUALES.")
        elif constraints:
            print(f"LAS TABLAS {t_name} SON IGUALES.")
        else:
            print(f"{t_name} no son iguales.")
except Error as e:
    print(f"Error en la base de datos: {e}")
finally:
    cursor.close()
    cursor2.close()
    conn.closeConexion()
    conn2.closeConexion()
