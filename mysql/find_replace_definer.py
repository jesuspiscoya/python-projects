import os
from dotenv import load_dotenv
from conexion import Conexion
from mysql.connector import Error

load_dotenv()

host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASS")
database = os.getenv("DB_DATABASE")

old_definer = input("Ingrese usuario antiguo: ")
new_definer = input("Ingrese usuario nuevo: ")

# Conexión a la base de datos
conn = Conexion(host, user, password, database)
conexion = conn.getConexion()

try:
    cursor = conexion.cursor()
    # Obtener los procedimientos almacenados
    cursor.execute(f"""
        SELECT ROUTINE_NAME, DEFINER, ROUTINE_TYPE
        FROM information_schema.ROUTINES
        WHERE ROUTINE_SCHEMA = '{database}'
        AND DEFINER = '{old_definer}@%';
    """)
    rows = cursor.fetchall()

    for proc_name, definer, proc_type in rows:
        # Obtener la definición completa del procedimiento
        cursor.execute(f"SHOW CREATE {proc_type} {proc_name};")
        create_statement = cursor.fetchone()[2]

        # Cambiar el DEFINER en la definición
        new_definition = create_statement.replace(old_definer, new_definer)

        # Eliminar el procedimiento antiguo
        cursor.execute(f"DROP {proc_type} IF EXISTS {proc_name};")

        # Crear el nuevo procedimiento con el nuevo DEFINER
        cursor.execute(new_definition)

        # Confirmar los cambios
        conexion.commit()

        print(f"{proc_type} actualizado: {proc_name}")
except Error as e:
    print(f"Error en la base de datos: {e}")
finally:
    cursor.close()
    conn.closeConexion()
