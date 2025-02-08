from datetime import date, timedelta
import os
import zipfile
import win32com.client

# Obtener la ruta del directorio de inicio del usuario
user_path = os.path.expanduser('~')
# Carpeta de destino
download_path = os.path.join(user_path, "Downloads")


def descargar_archivo():
    try:
        file_name = None

        # Conectarse a la aplicación de Outlook
        outlook = win32com.client.Dispatch("Outlook.Application")
        namespace = outlook.GetNamespace("MAPI")

        # Obtener la bandeja de entrada (6)
        inbox = namespace.GetDefaultFolder(6)

        menssages = inbox.Items
        # Ordenar los correos por fecha de recepción
        menssages.Sort("[ReceivedTime]", True)

        today = date.today() - timedelta(days=1)

        for message in menssages:
            # Buscar correo por el asunto
            if message.Subject == f"Laive Data {today}":
                print(f"Correo encontrado: {message.Subject}")

                for attachment in message.Attachments:
                    file_name = attachment.FileName
                    file_path = os.path.join(download_path, file_name)

                    # Guardar el archivo adjunto
                    attachment.SaveAsFile(file_path)
                    print(f"Archivo descargado: {file_name} en {file_path}")

                return file_name
    except AttributeError as e:
        print(f"Error al intentar acceder a Outlook: {e}")


def unzip_file(zip_name, output_path):
    print(f"Archivo a descomprimir: {zip_name}")
    zip_file = os.path.join(download_path, zip_name)
    print(f"Archivo encontrado: {zip_file}")

    # Descomprimir el archivo ZIP
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        # Obtener la lista de archivos extraídos
        for file_name in zip_ref.namelist():
            print(f"Archivo extraído: {file_name}")

        # Extrae todo el contenido en el directorio especificado
        zip_ref.extractall(output_path)

        print(f"Archivo descomprimido correctamente en {output_path}")

    # Eliminar el archivo ZIP original
    os.remove(zip_file)
    print(f"Archivo ZIP eliminado: {zip_file}")


file = descargar_archivo()
unzip_file(file, r"\\selloutapp\FTP\Moran")
