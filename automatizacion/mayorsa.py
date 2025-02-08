from datetime import date, timedelta
import os
import shutil
import time
import requests
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


def get_url_driver(url, wdriver):
    return wdriver.get(url)


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


def generar_csv(url, token, body, source):
    header = {"Authorization": f"Bearer {token}"}
    json = {
        "reportDownloadingTitle": f"{source}-SMU_{today}",
        "fileType": "csv",
        "delimiter": ",",
        "dimensions": "D_DAY,D_MONTH,D_WEEK,D_YEAR,P_PRODUCT,P_PRODUCT_CODE,P_PRODUCT_DESC,P_PRODUCT_EAN,P_CATEGORY_1,P_CATEGORY_2,P_CATEGORY_3,P_CATEGORY_4,C_PRODUCT_STATUS,S_STORE,S_STORE_CODE,S_STORE_DESC,S_CATEGORY_1"
    }
    json = json | body

    res = requests.post(url, json=json, headers=header, timeout=60)

    if res.status_code == 200:
        print(f"Se generó el archivo de {source} con éxito.")
    else:
        print(f"{res.json().get('message')}")


def descargar_archivo(xpath, source, today, file_name):
    print(f'Descargando archivo de {source}...')

    # Descargar archivo
    espera_explicita_element(driver, xpath).find_element(
        By.PARTIAL_LINK_TEXT, f'{source}-SMU_{today}').click()

    time.sleep(5)

    # Obtener la ruta del directorio de inicio del usuario
    directorio_usuario = os.path.expanduser('~')
    # Construir la ruta completa del directorio de descargas
    ruta_origen = os.path.join(directorio_usuario, 'Downloads')
    ruta_destino = r'\\selloutapp\FTP\Moderno\MAYORSA'

    # Verificar si el directorio de descargas existe
    if os.path.exists(ruta_origen):
        files = os.listdir(ruta_origen)
        name = [f for f in files if f'{source}-SMU_{today}' in f]
        file = os.path.join(ruta_origen, name[0])

        if os.path.exists(file):
            print(f"Archivo encontrado: {file}")

            # Cambiar el nombre del archivo
            os.rename(file, os.path.join(ruta_origen, file_name))

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
    return


# Credenciales de acceso
user = os.getenv("USER_MAYORSA")
psw = os.getenv("PASS_MAYORSA")

driver = abrir_navegador()
url_login = 'https://smu.portal2b.com/views/2'
get_url_driver(url_login, driver)

xpath_username = '//input[@id="user_email"]'
e_username = espera_explicita_element(driver, xpath_username)
e_username.clear()
e_username.send_keys(user)

xpath_pass = '//input[@id="user_password"]'
e_pass = espera_explicita_element(driver, xpath_pass)
e_pass.clear()
e_pass.send_keys(psw)

# Click en iniciar login de credenciales
xpath_submit = '//*[@id="new_user"]/div/div[5]/button'
espera_explicita_element(driver, xpath_submit).click()

time.sleep(2)

xpath_borrar = '//iframe[@id="tableau"]'
iframe = espera_explicita_element(driver, xpath_borrar)
driver.switch_to.frame(iframe)

# Obtener la URL dentro del iframe utilizando JavaScript
url_iframe = driver.execute_script('return window.location.href')
url_token = url_iframe.replace('https://downloaders-frontend-smu.portal2b.com/sales-smu#access_token',
                               'https://downloaders-backend-smu.portal2b.com/api/login?id').replace('&token_type=Bearer&expires_in=86400', '')

response = requests.get(url_token, timeout=60)
data = response.json()
today = date.today()

if response.status_code == 200:
    generar_csv('https://downloaders-backend-smu.portal2b.com/api/reports/generate_smu/stock',
                data.get('token'), {}, 'Stock')

    values = {
        "dates": {"from": str(today - timedelta(days=5)), "to": str(today)}
    }
    generar_csv('https://downloaders-backend-smu.portal2b.com/api/reports/generate_smu/sales',
                data.get('token'), values, 'Venta')

    time.sleep(70)

    # Ingresar a página de descarga
    get_url_driver('https://smu.portal2b.com/views?navbar=Descargador', driver)

    descargar_archivo('//div[@id="ventas"]', 'Venta',
                      today, 'VENTAS_MAYORSA.csv')

    descargar_archivo('//div[@id="inventarios"]',
                      'Stock', today, 'STOCK_MAYORSA.csv')
else:
    print(f"{data.get('message')}")

cerrar_driver_navegador(driver)
