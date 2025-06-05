import os
import time
import shutil
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


def move_excel(file_name):
    # Obtener la ruta del directorio de inicio del usuario
    user_directory = os.path.expanduser('~')
    # Construir la ruta completa del directorio de descargas
    ruta_origen = os.path.join(user_directory, 'Downloads')
    archivo_origen = os.path.join(ruta_origen, file_name)
    ruta_destino = r'\\selloutapp\FTP\Moderno\OXXO'
    archivo_destino = os.path.join(ruta_destino, 'VENTAS_OXXO.xlsx')

    # Verificar si el directorio de descargas existe
    if os.path.exists(archivo_origen):
        print(f"Archivo encontrado: {archivo_origen}")

        # Mover el archivo
        shutil.move(archivo_origen, ruta_destino)

        # Verificar si el archivo con el nuevo nombre ya existe
        if os.path.exists(archivo_destino):
            print(
                "El archivo VENTAS_OXXO.xlsx ya existe. Se eliminará y se sobrescribirá.")
            # Eliminar el archivo existente
            os.remove(archivo_destino)

        # Cambiar el nombre del archivo
        os.rename(os.path.join(ruta_destino, file_name), archivo_destino)

        print(f"Archivo movido correctamente en: {ruta_destino}")
    else:
        print(f"No se encontró el archivo {file_name}.")


driver = abrir_navegador()
url_login = 'https://outlook.office.com/mail/'
get_url_driver(url_login, driver)

# Credenciales de acceso
user = os.getenv("USER_OXXO")
psw = os.getenv("PASS_OXXO")

xpath_username = '//input[@id="i0116"]'
e_username = espera_explicita_element(driver, xpath_username)
# e_username.clear()
e_username.send_keys(user)

# Click en boton siguiente
xpath_next = '//input[@id="idSIButton9"]'
espera_explicita_element(driver, xpath_next).click()

xpath_pass = '//input[@id="i0118"]'
e_pass = espera_explicita_element(driver, xpath_pass)
# e_pass.clear()
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

xpath_show = '//*[@id="focused"]/div[2]/div/div/div/div/div/div/div/div[2]'
espera_explicita_element(driver, xpath_show).click()

xpath_donwload = '//*[@id="fluent-default-layer-host"]/div[3]/div/div/div/div/div/div/ul/li[6]'
espera_explicita_element(driver, xpath_donwload).click()

time.sleep(10)

move_excel('BaseInventario_LAIVE S.A. 10LIM.xlsx')

cerrar_driver_navegador(driver)
