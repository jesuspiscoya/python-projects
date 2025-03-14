import pyodbc


class Conexion:
    # Conexión a la base de datos
    def __init__(self, host, database):
        self.host = host
        self.database = database
        self.conexion = None

    def getConexion(self):
        conn_str = f"DRIVER={{SQL Server}};SERVER={
            self.host},1434;DATABASE={self.database};Trusted_Connection=yes"

        try:
            self.conexion = pyodbc.connect(conn_str)
            return self.conexion
        except pyodbc.Error as e:
            print(f"Error al conectar a SQL Server: {e}")
            exit()

    def closeConexion(self):
        self.conexion.close()
        print("Conexión cerrada.")
