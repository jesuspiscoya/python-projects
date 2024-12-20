import os
from dotenv import load_dotenv
from conexion import Conexion
from mysql.connector import Error

load_dotenv()

host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASS")
# db = os.getenv("DB_DATABASE")
databases = [
    "UTaskSupervisorDb",
    "dbapppdv_pro",
]

# old_definer = input("Ingrese usuario antiguo: ")
new_definer = input("Ingrese usuario nuevo: ")


for database in databases:
    # Conexión a la base de datos
    conn = Conexion(host, user, password, database)
    conexion = conn.getConexion()

    try:
        cursor = conexion.cursor()
        # Obtener los procedimientos almacenados y funciones
        cursor.execute(f"""
            SELECT ROUTINE_NAME, DEFINER, ROUTINE_TYPE
            FROM information_schema.ROUTINES
            WHERE ROUTINE_SCHEMA = '{database}'
            AND DEFINER != '{new_definer}@%';
        """)
        rows = cursor.fetchall()

        for proc_name, definer, proc_type in rows:
            # Obtener la definición completa del procedimiento
            cursor.execute(f"SHOW CREATE {proc_type} `{proc_name}`;")
            create_statement = cursor.fetchone()[2]

            # Cambiar el DEFINER en la definición
            new_definition = create_statement.replace(
                definer.rstrip("@%"), new_definer)

            # Eliminar el procedimiento y función antiguo
            cursor.execute(f"DROP {proc_type} IF EXISTS `{proc_name}`;")

            # Crear el nuevo procedimiento y función con el nuevo DEFINER
            cursor.execute(new_definition)

            # Confirmar los cambios
            conexion.commit()

            print(f"{proc_type} actualizado: {proc_name}")

        cursor2 = conexion.cursor()
        # Obtener las vistas
        cursor2.execute(f"""
            SELECT TABLE_NAME, DEFINER
            FROM information_schema.VIEWS
            WHERE TABLE_SCHEMA = '{database}'
            AND DEFINER != '{new_definer}@%';
        """)
        rows2 = cursor2.fetchall()

        for view_name, definer in rows2:
            # Obtener la definición completa de la vista
            cursor2.execute(f"SHOW CREATE VIEW `{view_name}`;")
            create_statement = cursor2.fetchone()[1]

            # Cambiar el DEFINER en la definición
            new_definition = create_statement.replace(
                definer.rstrip("@%"), new_definer)

            # Eliminar la vista antigua
            cursor2.execute(f"DROP VIEW IF EXISTS `{view_name}`;")

            # Crear la nueva vista con el nuevo DEFINER
            cursor2.execute(new_definition)

            # Confirmar los cambios
            conexion.commit()

            print(f"VIEW actualizada: {view_name}")

        cursor3 = conexion.cursor()
        # Obtener los eventos
        cursor3.execute(f"""
            SELECT EVENT_NAME, DEFINER
            FROM information_schema.EVENTS
            WHERE EVENT_SCHEMA = '{database}'
            AND DEFINER != '{new_definer}@%';
        """)
        rows3 = cursor3.fetchall()

        for event_name, definer in rows3:
            # Obtener la definición completa del evento
            cursor3.execute(f"SHOW CREATE EVENT `{event_name}`;")
            create_statement = cursor3.fetchone()[3]

            # Cambiar el DEFINER en la definición
            new_definition = create_statement.replace(
                definer.rstrip("@%"), new_definer)

            # Eliminar el evento antiguo
            cursor3.execute(f"DROP EVENT IF EXISTS `{event_name}`;")

            # Crear el nuevo evento con el nuevo DEFINER
            cursor3.execute(new_definition)

            # Confirmar los cambios
            conexion.commit()

            print(f"EVENT actualizado: {event_name}")

        cursor4 = conexion.cursor()
        # Obtener los triggers
        cursor4.execute(f"""
            SELECT TRIGGER_NAME, DEFINER
            FROM information_schema.TRIGGERS
            WHERE TRIGGER_SCHEMA = '{database}'
            AND DEFINER != '{new_definer}@%';
        """)
        rows4 = cursor4.fetchall()

        for trigger_name, definer in rows4:
            # Obtener la definición completa del trigger
            cursor4.execute(f"SHOW CREATE TRIGGER `{trigger_name}`;")
            create_statement = cursor4.fetchone()[2]

            # Cambiar el DEFINER en la definición
            new_definition = create_statement.replace(
                definer.rstrip("@%"), new_definer)

            # Eliminar el trigger antiguo
            cursor4.execute(f"DROP TRIGGER IF EXISTS `{trigger_name}`;")

            # Crear el nuevo trigger con el nuevo DEFINER
            cursor4.execute(new_definition)

            # Confirmar los cambios
            conexion.commit()

            print(f"TRIGGER actualizado: {trigger_name}")
    except Error as e:
        print(f"Error en la base de datos: {e}")
    finally:
        cursor.close()
        cursor2.close()
        cursor3.close()
        cursor4.close()
        conn.closeConexion()
