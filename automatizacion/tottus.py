import os
import time
import shutil
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
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


def get_url_driver(url, wdriver):
    return wdriver.get(url)


def cerrar_driver_navegador(wdriver):
    wdriver.close()
    return wdriver.quit()


def espera_explicita_element(wdriver, xpath):
    try:
        wait = WebDriverWait(wdriver, 30)
        wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        element = wdriver.find_element(By.XPATH, xpath)
        return element
    except TimeoutException:
        print("Espera explicita, timeout de elemento: " + xpath)
    except NoSuchElementException:
        print("Espera explicita, no se encontro o no se visualizo el elemento: " + xpath)


def login_tottus():
    # Credenciales de acceso
    user = os.getenv("USER_TOTTUS")
    psw = os.getenv("PASS_TOTTUS")

    xpath_username = '//input[@id="username"]'
    e_username = espera_explicita_element(driver, xpath_username)
    e_username.send_keys(user)

    xpath_pass = '//input[@id="password"]'
    e_pass = espera_explicita_element(driver, xpath_pass)
    e_pass.send_keys(psw)

    # Click en iniciar login de credenciales
    xpath_submit = '//*[@id="loginForm"]/div[4]/div/button'
    espera_explicita_element(driver, xpath_submit).click()


def select_report(report_name):
    driver.switch_to.default_content()

    # Ingresar a Descargables
    xpath_downloadable = '//*[@id="single-spa-application:reports"]/div[2]/div/div[2]/div/div/div/div[2]/div/div/div/div/div/div/div/header/button[3]'
    espera_explicita_element(driver, xpath_downloadable).click()

    # Ingresar al reporte
    espera_explicita_element(driver, report_name).click()

    time.sleep(10)

    # Cambiar a iframe de Looker Studio
    driver.switch_to.frame(0)


def download_report():
    xpath_table = '//*[@id="dashboard-layout-wrapper"]'
    table = espera_explicita_element(driver, xpath_table)

    hover = ActionChains(driver)
    hover.move_to_element(table).perform()

    # Seleccionar mostrar más acciones
    xpath_more = '//*[@id="styled-tile-dashboard"]/div/section/div/div[1]/div/button[1]'
    espera_explicita_element(driver, xpath_more).click()

    # Seleccionar Download data
    xpath_download_data = '/html/body/div[3]/div/div/div/div/div/ul/li[1]'
    espera_explicita_element(driver, xpath_download_data).click()

    time.sleep(3)

    # Seleccionar Advanced data options
    xpath_options = '/html/body/div[3]/div/div/div[2]/div/div/div/div[2]/div/div'
    espera_explicita_element(driver, xpath_options).click()

    # Seleccionar Unformatted data
    xpath_unformatted = '/html/body/div[3]/div/div/div[2]/div/div/div/div[2]/div/div[2]/div/div/div[2]/div[1]/div/div/div[2]'
    espera_explicita_element(driver, xpath_unformatted).click()

    # Seleccionar all results
    xpath_all = '/html/body/div[3]/div/div/div[2]/div/div/div/div[2]/div/div[2]/div/div/div[3]/div[1]/div/div/div[2]'
    espera_explicita_element(driver, xpath_all).click()

    xpath_download = '//*[@id="qr-export-modal-download"]'
    espera_explicita_element(driver, xpath_download).click()

    time.sleep(30)


def move_csv(file_name_origen, file_name_destino):
    # Obtener la ruta del directorio de inicio del usuario
    user_directory = os.path.expanduser('~')
    # Construir la ruta completa del directorio de descargas
    ruta_origen = os.path.join(user_directory, 'Downloads')
    archivo_origen = os.path.join(ruta_origen, file_name_origen)
    ruta_destino = r'\\selloutapp\FTP\Moderno\TOTTUS'
    archivo_destino = os.path.join(ruta_destino, file_name_destino)

    # Verificar si el directorio de descargas existe
    if os.path.exists(archivo_origen):
        print(f"Archivo encontrado: {archivo_origen}")

        # Mover el archivo
        shutil.move(archivo_origen, ruta_destino)

        # Verificar si el archivo con el nuevo nombre ya existe
        if os.path.exists(archivo_destino):
            print(
                f"El archivo {file_name_destino} ya existe. Se eliminará y se sobrescribirá.")
            # Eliminar el archivo existente
            os.remove(archivo_destino)

        # Cambiar el nombre del archivo
        os.rename(os.path.join(ruta_destino, file_name_origen), archivo_destino)

        print(f"Archivo movido correctamente en: {ruta_destino}")
    else:
        print(f"No se encontró el archivo {file_name_origen}.")


driver = abrir_navegador()
url_login = 'https://fbusinesscenter.com/login'
get_url_driver(url_login, driver)

login_tottus()

# Ingresar a pestaña Market Insights
xpath_reports = '//*[@id="single-spa-application:home"]/div[2]/div/div[2]/div[1]/div[2]'
espera_explicita_element(driver, xpath_reports).click()

# Ingresar al reporte de Ventas Diarias
select_report(
    '//*[@id="popover-484f5b57-01e0-4be7-8a50-ed6d22d98d1a"]/div[3]/button[2]')

# Seleccionar Fecha
xpath_date = '//*[@id="lk-react-container"]/div/div/div/section/div/div[1]/div/div[2]/section/div/div[1]/div/span'
espera_explicita_element(driver, xpath_date).click()

# Seleccionar Últimos 7 días
xpath_week = '//*[@id="panel-0"]/div/ul/li[3]'
week = espera_explicita_element(driver, xpath_week).click()

time.sleep(3)

# Actualizar datos
xpath_body = '//*[@id="lk-layout-embed"]'
espera_explicita_element(driver, xpath_body).send_keys(
    Keys.CONTROL + Keys.SHIFT + Keys.ENTER)

time.sleep(8)

download_report()

# Mover el archivo descargado a la ruta de destino
move_csv('Ventas diarias.csv', 'venta_tottus.csv')

# Ingresar al reporte de Stock de hoy
select_report(
    '//*[@id="popover-484f5b57-01e0-4be7-8a50-ed6d22d98d1a"]/div[3]/button[5]')

download_report()

# Mover el archivo descargado a la ruta de destino
move_csv('Descargable instock.csv', 'stock_tottus.csv')

# Ingresar al reporte de Maestro de Productos
select_report(
    '//*[@id="popover-484f5b57-01e0-4be7-8a50-ed6d22d98d1a"]/div[3]/button[6]')

download_report()

# Mover el archivo descargado a la ruta de destino
move_csv('Maestro de productos.csv', 'productos_tottus.csv')

cerrar_driver_navegador(driver)
