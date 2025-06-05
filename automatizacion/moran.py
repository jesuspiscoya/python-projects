import os
import time
import zipfile
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

load_dotenv()


def abrir_navegador():
    # navegador - configuracion
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-browser-side-navigation")
    options.add_argument("--disable-gpu")

    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    }
    options.add_experimental_option("prefs", prefs)

    wdriver = webdriver.Chrome(options=options)
    wdriver.maximize_window()
    return wdriver


def get_url_driver(URL, wdriver):
    return wdriver.get(URL)


def cerrar_driver_navegador(wdriver):
    wdriver.close()
    return wdriver.quit()


def espera_explicita_element(wdriver, xpath):
    try:
        wait = WebDriverWait(wdriver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        element = wdriver.find_element(By.XPATH, xpath)
        return element
    except TimeoutException:
        print("Espera explicita, timeout de elemento: " + xpath)
    except NoSuchElementException:
        print("Espera explicita, no se encontro o no se visualizo el elemento: " + xpath)


def unzip_doc():
    # Obtener la ruta del directorio de inicio del usuario
    directorio_usuario = os.path.expanduser('~')
    # Construir la ruta completa del directorio de descargas
    ruta_origen = os.path.join(directorio_usuario, 'Downloads')
    ruta_destino = r'\\selloutapp\FTP\Moran'

    # Verificar si el directorio de descargas existe
    if os.path.exists(ruta_origen):
        zip_file = os.path.join(ruta_origen, "MDSA_DATOS.zip")

        if zip_file != "":
            print(f"Archivo encontrado: {zip_file}")

            # Descomprimir el archivo ZIP
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                # Obtener la lista de archivos extraídos
                for file_name in zip_ref.namelist():
                    print(f"Archivo extraído: {file_name}")

                # Extrae todo el contenido en el directorio especificado
                zip_ref.extractall(ruta_destino)

                print(f"Archivo descomprimido correctamente en {ruta_destino}")

            # Eliminar el archivo ZIP original
            os.remove(zip_file)
            print(f"Archivo ZIP eliminado: {zip_file}")
        else:
            print("No se encontró el archivo ZIP")
    else:
        print("No se pudo encontrar la ruta del directorio de descargas.")


driver = abrir_navegador()
url_login = 'https://outlook.office.com/mail/'
get_url_driver(url_login, driver)

# Credenciales de acceso
user = os.getenv("USER_MORAN")
psw = os.getenv("PASS_MORAN")

xpath_username = '//input[@id="i0116"]'
e_username = espera_explicita_element(driver, xpath_username)
e_username.clear()
e_username.send_keys(user)

# Click en boton siguiente
xpath_next = '//input[@id="idSIButton9"]'
espera_explicita_element(driver, xpath_next).click()

xpath_pass = '//input[@id="i0118"]'
e_pass = espera_explicita_element(driver, xpath_pass)
e_pass.clear()
e_pass.send_keys(psw)

# Click en boton siguiente
xpath_submit = '//input[@id="idSIButton9"]'
espera_explicita_element(driver, xpath_submit).click()

xpath_no = '//input[@id="idBtn_Back"]'
espera_explicita_element(driver, xpath_no).click()

time.sleep(10)

xpath_first_mail = '//*[@id="MailList"]/div/div/div/div/div/div/div/div[2]'
espera_explicita_element(driver, xpath_first_mail).click()

time.sleep(10)

xpath_donwload = '//*[@id="focused"]/div[2]/div/div/div/div/div'
espera_explicita_element(driver, xpath_donwload).click()

time.sleep(15)

unzip_doc()

cerrar_driver_navegador(driver)
