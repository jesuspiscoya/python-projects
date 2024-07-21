import datetime
import json
import os
import pandas as pd
from dotenv import load_dotenv
from mysql.connector import Error
from conexion import Conexion

load_dotenv()

host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASS")
database = os.getenv("DB_DATABASE")

idDistribuidora = input("Ingrese distribuidora: ")
codVendedor = input("Ingrese vendedor: ")
codCliente = input("Ingrese cliente: ")
fecha = f"%{datetime.datetime.now().strftime("%Y-%m-%d")}%"

# idDistribuidora = '1'
# codVendedor = '021'
# codCliente = '110750'
# fecha = '%2024-07-19%'

# Conexión a la base de datos
conn = Conexion(host, user, password, database)
conexion = conn.getConexion()

codProductos = []
cantidadProductos = []

df = pd.read_excel("pedido.xlsx")

# Recuperar pedido
try:
    cursor = conexion.cursor()
    SQL = """
    SELECT fechacrea, request
    FROM logmobile
    WHERE iddistribuidora = %s
        AND codigovendedor = %s
        AND codigocliente = %s
        AND origen='CrearPedido'
        AND fechacrea like %s
        ORDER BY fechacrea DESC;
    """
    values = (idDistribuidora, codVendedor, codCliente, fecha)
    cursor.execute(SQL, values)
    rows = cursor.fetchall()

    for pedido in rows:
        diccionario = json.loads(pedido[1])
        codProductos.append(diccionario['CodigoProducto'])
        cantidadProductos.append(diccionario['NuevaCantidad'])

        if diccionario['IdPedido'] == 0:
            break

except Error as e:
    print(f"Error al recuperar pedido: {e}")
finally:
    cursor.close()
    conn.closeConexion()

codProductos.reverse()
cantidadProductos.reverse()

indices_a_eliminar = []
vistos = set()

# Iterar sobre los códigos de productos en reversa
for index in reversed(range(len(codProductos))):
    codigo = codProductos[index]
    if codigo in vistos:
        indices_a_eliminar.append(index)
    else:
        vistos.add(codigo)

# Eliminar elementos de las listas usando los índices recolectados
for index in indices_a_eliminar:
    print(f"Eliminado: {codProductos[index]}: {cantidadProductos[index]}")
    del codProductos[index]
    del cantidadProductos[index]

# Ajustar el dataframe con la misma cantidad de elementos
df = df.head(len(codProductos))

# Actualizar el dataframe
df['CÓDIGO'] = codProductos
df['CANTIDAD'] = cantidadProductos

# Escribir en el archivo excel
df.to_excel("pedido.xlsx", index=False)
