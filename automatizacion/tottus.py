import os
import shutil
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


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


def descarga_archivo(url, file_name):
    # Ingresar a página de descarga
    get_url_driver(url, driver)

    # Descargar archivo
    xpath_file = '//*[@id="row"]/tbody/tr[1]/td/a'
    button_download = espera_explicita_element(driver, xpath_file)
    button_download.click()

    txt_name = button_download.get_attribute('href').replace(
        'https://b2b.tottus.com/b2btopepr/servlet/download/', '')

    time.sleep(5)

    # Obtener la ruta del directorio de inicio del usuario
    directorio_usuario = os.path.expanduser('~')
    # Construir la ruta completa del directorio de descargas
    ruta_origen = os.path.join(directorio_usuario, 'Downloads')
    ruta_destino = r'C:\Users\jpiscoya\Music'

    # Verificar si el directorio de descargas existe
    if os.path.exists(ruta_origen):
        txt_origen = os.path.join(ruta_origen, txt_name)

        if os.path.exists(txt_origen):
            print(f"Archivo encontrado: {txt_origen}")

            # Cambiar el nombre del archivo
            os.rename(txt_origen, os.path.join(ruta_origen, file_name))

            nuevo_nombre = os.path.join(ruta_destino, file_name)

            # Verificar si el archivo con el nuevo nombre ya existe
            if os.path.exists(nuevo_nombre):
                print(f"El archivo {
                      file_name} ya existe. Se eliminará y se sobrescribirá.")
                # Eliminar el archivo existente
                os.remove(nuevo_nombre)

            # Mover el archivo
            shutil.move(os.path.join(ruta_origen, file_name), ruta_destino)
        else:
            print("No se encontró el archivo.")
    else:
        print("No se pudo encontrar la ruta del directorio de descargas.")


driver = abrir_navegador()
url_login = 'https://b2b.tottus.com/b2btoclpr/grafica/html/main_home.html'
get_url_driver(url_login, driver)

# Escritura de elementos - Credenciales
company = '20100095450'
username = '10020310'
pwd = 'Lcuesta@25'

# Seleccionar B2B Tottus Perú
xpath_select = '//*[@id="CADENA"]'
Select(espera_explicita_element(driver, xpath_select)
       ).select_by_visible_text('Tottus Perú')

xpath_company = '//*[@id="empresa"]'
e_company = espera_explicita_element(driver, xpath_company)
e_company.clear()
e_company.send_keys(company)

xpath_username = '//*[@id="usuario"]'
e_username = espera_explicita_element(driver, xpath_username)
e_username.clear()
e_username.send_keys(username)

xpath_pass = '//*[@id="clave"]'
e_pass = espera_explicita_element(driver, xpath_pass)
e_pass.clear()
e_pass.send_keys(pwd)

# Click en iniciar login de credenciales
xpath_submit = '//*[@id="entrar2"]'
espera_explicita_element(driver, xpath_submit).click()

time.sleep(5)

# Descargar archivo de Ventas
descarga_archivo(
    'https://b2b.tottus.com/b2btopepr/logica/jsp/B2BvFDescarga.do?tipo=eVTA&opcId=223', 'venta_tottus.txt')

# Descargar archivo de Stock
descarga_archivo(
    'https://b2b.tottus.com/b2btopepr/logica/jsp/B2BvFDescarga.do?tipo=eCAT', 'stock_tottus.txt')

cerrar_driver_navegador(driver)
