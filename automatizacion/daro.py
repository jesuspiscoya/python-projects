import os
from ftplib import FTP
from dotenv import load_dotenv

load_dotenv()

# Datos de conexión
host = os.getenv("FTP_HOST")
user = os.getenv("FTP_USER")
psw = os.getenv("FTP_PASS")

# Archivo local y remoto
PATH_LOCAL = r'C:\Users\jpiscoya\Downloads\daro'
PATH_REMOTE = 'FTP_DARO'
# Conectarse al servidor FTP
ftp = FTP(host)
ftp.login(user, psw)

# Cambiar al directorio específico en el servidor FTP
ftp.cwd(PATH_REMOTE)

# Obtener todos los archivos de la carpeta local
for local_file in os.listdir(PATH_LOCAL):
    # Ruta completa del archivo local
    local_file_path = os.path.join(PATH_LOCAL, local_file)

    # Verificar que sea un archivo (y no un directorio u otro tipo de archivo)
    if os.path.isfile(local_file_path):
        # Abrir el archivo local en modo binario
        with open(local_file_path, 'rb') as f:
            # Subir el archivo al servidor FTP, sobreescribiendo si existe
            ftp.storbinary(f'STOR {local_file}', f)
            print(f"Archivo {local_file} subido exitosamente.")

# Cerrar la conexión FTP
ftp.quit()
