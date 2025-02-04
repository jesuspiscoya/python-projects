import os
from ftplib import FTP

# Datos de conexión
FTP_HOST = 'sellout.laive.pe'
FTP_USER = 'ftp_daro'
FTP_PASS = 'D4skh3lp#X'

# Archivo local y remoto
PATH_LOCAL = r'C:\Users\jpiscoya\Downloads\daro'
PATH_REMOTE = 'FTP_DARO'
# Conectarse al servidor FTP
ftp = FTP(FTP_HOST)
ftp.login(FTP_USER, FTP_PASS)

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
