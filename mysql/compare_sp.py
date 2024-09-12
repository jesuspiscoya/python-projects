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

storage_procedures_list = [
    'sp_get_complete_request_list',
    'sp_get_next_request_code',
    'sp_get_products_sap',
    'sp_get_products_uniflex',
    'sp_get_request',
    'sp_get_request_application',
    'sp_get_request_application_by_id',
    'sp_get_request_application_by_request_id',
    'sp_get_request_by_id',
    'sp_get_request_change_all_suppliers',
    'sp_get_request_change_by_suppliers',
    'sp_get_request_change_national',
    'sp_get_request_channel',
    'sp_get_request_channel_by_id',
    'sp_get_request_detail',
    'sp_get_request_detail_by_id',
    'sp_get_request_detail_by_request_id',
    'sp_get_request_new_all_suppliers',
    'sp_get_request_new_national',
    'sp_get_request_reason',
    'sp_get_request_reason_by_id',
    'sp_get_request_state',
    'sp_get_request_state_by_id',
    'sp_get_request_type',
    'sp_get_request_type_by_id',
    'sp_insert_process_log',
    'sp_process_generate_history',
    'sp_process_generate_history_lima',
    'sp_process_generate_history_lima_exceptions',
    'sp_process_generate_history_province',
    'sp_process_generate_history_province_exceptions',
    'sp_process_pricelist_new_prices',
    'sp_process_pricelist_new_prices_national',
    'sp_process_pricelist_request_and_sync_prices',
    'sp_process_pricelist_request_and_sync_prices_by_supplier',
    'sp_process_pricelist_request_and_sync_prices_national',
    'sp_process_price_list_request',
    'sp_recalculate_all_price_list',
    'sp_recalculate_all_supplier_prices_lima',
    'sp_recalculate_all_supplier_prices_province',
    'sp_reset_changes',
]


def get_sp_ddl(cursor_1, cursor_2, sp_name):
    try:
        cursor_1.execute(f"""
            SELECT DEFINER,ROUTINE_DEFINITION
            FROM INFORMATION_SCHEMA.ROUTINES
            WHERE ROUTINE_NAME = '{sp_name}'
            AND ROUTINE_TYPE = 'PROCEDURE'
            AND ROUTINE_SCHEMA = '{database}'
        """)
        list_string = cursor_1.fetchone()[1].strip().split()
        ddl1 = " ".join(list_string)

        cursor_2.execute(f"""
            SELECT DEFINER,ROUTINE_DEFINITION
            FROM INFORMATION_SCHEMA.ROUTINES
            WHERE ROUTINE_NAME = '{sp_name}'
            AND ROUTINE_TYPE = 'PROCEDURE'
            AND ROUTINE_SCHEMA = '{database2}'
        """)
        list_string = cursor_2.fetchone()[1].strip().split()
        ddl2 = " ".join(list_string)

        if ddl1 == ddl2:
            return True
        else:
            return False
    except:
        # print(f"El SP {sp_name} no existe.")
        return None


def get_fn_ddl(cursor_1, cursor_2, fn_name):
    try:
        cursor_1.execute(f"""
            SELECT DEFINER,ROUTINE_DEFINITION
            FROM INFORMATION_SCHEMA.ROUTINES
            WHERE ROUTINE_NAME = '{fn_name}'
            AND ROUTINE_TYPE = 'FUNCTION'
            AND ROUTINE_SCHEMA = '{database}'
        """)
        list_string = cursor_1.fetchone()[1].strip().split()
        ddl1 = " ".join(list_string)

        cursor_2.execute(f"""
            SELECT DEFINER,ROUTINE_DEFINITION
            FROM INFORMATION_SCHEMA.ROUTINES
            WHERE ROUTINE_NAME = '{fn_name}'
            AND ROUTINE_TYPE = 'FUNCTION'
            AND ROUTINE_SCHEMA = '{database2}'
        """)
        list_string = cursor_2.fetchone()[1].strip().split()
        ddl2 = " ".join(list_string)

        if ddl1 == ddl2:
            return True
        else:
            return False
    except:
        print(f"El SP o FN {fn_name} no existe.")
        return None


try:
    cursor = conexion.cursor()
    cursor2 = conexion2.cursor()

    for s_name in storage_procedures_list:
        storage_procedures = get_sp_ddl(cursor, cursor2, s_name)
        functions = None

        if storage_procedures is None:
            functions = get_fn_ddl(cursor, cursor2, s_name)
            if functions is None:
                continue

        if storage_procedures:
            print(f"LOS SP {s_name} SON IGUALES.")
        elif functions:
            print(f"LOS FN {s_name} SON IGUALES.")
        else:
            print(f"{s_name} no son iguales.")
except Error as e:
    print(f"Error en la base de datos: {e}")
finally:
    cursor.close()
    cursor2.close()
    conn.closeConexion()
    conn2.closeConexion()
