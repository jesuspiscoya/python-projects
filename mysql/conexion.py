import mysql.connector as conn
from mysql.connector import Error

# Conexión a la base de datos
class Conexion:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conexion = None

    def getConexion(self):
        try:
            self.conexion = conn.connect(
                host=self.host,
                user=self.user,
                passwd=self.password,
                database=self.database
            )

            if self.conexion.is_connected():
                print("Conexión exitosa.")

            return self.conexion

        except Error as e:
            print(f"Error al conectar a MySQL: {e}")
            exit()


    def closeConexion(self):
        if self.conexion.is_connected():
            self.conexion.close()
            print("Conexión cerrada.")
