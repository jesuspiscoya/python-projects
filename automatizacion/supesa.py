import os
import time
import zipfile
from datetime import date, timedelta
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
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


def seleccionar_mes_anterior():
    xpath_before_month = '//*[@id="PID_VAADIN_POPUPCAL"]/tbody/tr[1]/td[2]/button'
    espera_explicita_element(driver, xpath_before_month).click()

    xpath_tabla_cal = '//table[@id="PID_VAADIN_POPUPCAL"]/tbody/tr[2]/td/table/tbody'
    values_tabla = espera_explicita_element(driver, xpath_tabla_cal)
    days = values_tabla.find_elements(
        By.CSS_SELECTOR, '.v-datefield-calendarpanel-day')

    days_copy = days.copy()

    for ele in days_copy:
        if ele.text != f'{date.today().day}':
            days.remove(ele)
        else:
            break

    return days


def seleccionar_fechas(xpath, num_days):
    espera_explicita_element(driver, xpath).click()

    today = date.today()
    primer_dia_mes = today.replace(day=1)

    if primer_dia_mes.weekday() == 0 and today.day < 6:
        days = seleccionar_mes_anterior()
    elif primer_dia_mes.weekday() == 1 and today.day < 5:
        days = seleccionar_mes_anterior()
    elif primer_dia_mes.weekday() == 2 and today.day < 4:
        days = seleccionar_mes_anterior()
    elif primer_dia_mes.weekday() == 3 and today.day < 3:
        days = seleccionar_mes_anterior()
    elif primer_dia_mes.weekday() == 4 and today.day < 2:
        days = seleccionar_mes_anterior()
    else:
        xpath_tabla_cal = '//table[@id="PID_VAADIN_POPUPCAL"]/tbody/tr[2]/td/table/tbody'
        values_tabla = espera_explicita_element(driver, xpath_tabla_cal)
        days = values_tabla.find_elements(
            By.CSS_SELECTOR, '.v-datefield-calendarpanel-day')

    if today.day > 6:
        days_copy = days.copy()

        for ele in days_copy:
            if ele.text != "1":
                days.remove(ele)
            else:
                break

    yesterday = today - timedelta(days=num_days)

    for ele in days:
        if ele.text == str(yesterday.day):
            ele.click()
            break


def boton_descarga(xpath):
    xpath_descarga = '//*[@id="SupermercadosBBRecommercemain-1228722670"]/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div[3]/div/div/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div[2]/div/div/div/div/div[1]/div/div/div[3]/div/div[1]/div'
    espera_explicita_element(driver, xpath_descarga).click()

    # Selecciona Descarga Dato Fuente Periodo
    espera_explicita_element(driver, xpath).click()


def cerrar_ventana(source):
    print(f"Error generando el archivo de {source}.")

    # Cerrar ventana emergente de error
    xpath_close = '//*[@id="SupermercadosBBRecommercemain-1228722670-overlays"]/div[3]/div/div/div[2]/div[2]'
    espera_explicita_element(driver, xpath_close).click()

    if source == "stock":
        boton_descarga(
            '//*[@id="SupermercadosBBRecommercemain-1228722670-overlays"]/div[2]/div/div/div[2]/div')

        # Descarga y descomprime archivo zip de Stock
        unzip_doc(
            '//*[@id="SupermercadosBBRecommercemain-1228722670-overlays"]/div[3]/div/div/div[3]/div/div/div[3]/div/div[1]', 'stock', 'stock_supesa.csv')
    else:
        boton_descarga(
            '//*[@id="SupermercadosBBRecommercemain-1228722670-overlays"]/div[2]/div/div/div[3]')

        # Seleccionar 5 días antes
        seleccionar_fechas(
            '//*[@id="SupermercadosBBRecommercemain-1228722670-overlays"]/div[3]/div/div/div[3]/div/div/div/div/div/div/div/div[3]/div/div[3]/div/div[3]/div/div/div/button', 5)

        # Descarga y descomprime archivo zip de Ventas
        unzip_doc('//*[@id="SupermercadosBBRecommercemain-1228722670-overlays"]/div[3]/div/div/div[3]/div/div/div/div/div/div/div/div[9]/div/div/div[1]/div', 'ventas', 'venta_supesa.csv')


def unzip_doc(xpath, source, file_name):
    espera_explicita_element(driver, xpath).click()

    time.sleep(10)

    # Descargar archivo zip de Ventas
    xpath_zip = '//*[@id="SupermercadosBBRecommercemain-1228722670-overlays"]/div[3]/div/div/div[3]/div/div/div/div/div/div/div/div/div/div/div[2]/div'
    element = espera_explicita_element(driver, xpath_zip)
    zip_name = element.text

    if zip_name != "Error generando el archivo.":
        element.click()
    else:
        cerrar_ventana(source)
        return

    # Obtener la ruta del directorio de inicio del usuario
    directorio_usuario = os.path.expanduser('~')
    # Construir la ruta completa del directorio de descargas
    ruta_origen = os.path.join(directorio_usuario, 'Downloads')
    ruta_destino = r'\\selloutapp\FTP\Moderno\SUPESA'

    # Verificar si el directorio de descargas existe
    if os.path.exists(ruta_origen):
        time.sleep(10)

        zip_file = os.path.join(ruta_origen, zip_name)

        if zip_name != "":
            print(f"Archivo encontrado: {zip_file}")

            # Descomprimir el archivo ZIP
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                # Obtener la lista de archivos extraídos
                archivo_extraido = zip_ref.namelist()[0]
                nuevo_nombre = os.path.join(ruta_destino, file_name)
                print(f"Archivo extraído: {archivo_extraido}")

                # Extrae todo el contenido en el directorio especificado
                zip_ref.extractall(ruta_destino)

                # Verificar si el archivo con el nuevo nombre ya existe
                if os.path.exists(nuevo_nombre):
                    print(f"El archivo {
                          nuevo_nombre} ya existe. Se eliminará y se sobrescribirá.")
                    # Eliminar el archivo existente
                    os.remove(nuevo_nombre)

                # Cambiar el nombre del archivo extraído
                os.rename(os.path.join(ruta_destino,
                                       archivo_extraido), nuevo_nombre)

                print(f"Archivo descomprimido correctamente en {ruta_destino}")

            # Eliminar el archivo ZIP original
            os.remove(zip_file)
            print(f"Archivo ZIP eliminado: {zip_file}")
        else:
            print("No se encontró el archivo ZIP")
    else:
        print("No se pudo encontrar la ruta del directorio de descargas.")


driver = abrir_navegador()
url_login = 'https://b2b.intercorpretail.pe/Supermercados/BBRe-commerce/main'
get_url_driver(url_login, driver)

# Escritura de elementos - Credenciales
username = 'mmendoza@laive.com.pe'
pwd = 'Laive2025'

xpath_username = '//input[@id="username"]'
e_username = espera_explicita_element(driver, xpath_username)
e_username.clear()
e_username.send_keys(username)

xpath_pass = '//input[@id="password"]'
e_pass = espera_explicita_element(driver, xpath_pass)
e_pass.clear()
e_pass.send_keys(pwd)

# Click en iniciar login de credenciales
xpath_submit = '//input[@id="kc-login"]'
espera_explicita_element(driver, xpath_submit).click()

time.sleep(8)

# Ingresar a pestaña comercial
xpath_comercial = '//*[@id="SupermercadosBBRecommercemain-1228722670"]/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div[1]/div/div/div[3]/div/span[3]'
espera_explicita_element(driver, xpath_comercial).click()

time.sleep(2)

# Ingresar a subpestaña ventas
xpath_ventas = '//*[@id="SupermercadosBBRecommercemain-1228722670-overlays"]/div[2]/div/div/span[2]'
espera_explicita_element(driver, xpath_ventas).click()

# Desmarcar checkbox de productos activos
xpath_activos = '//*[@id="SupermercadosBBRecommercemain-1228722670"]/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div[3]/div/div/div/div/div[2]/div/div/div/div/div/div/div[1]/div/div[1]/div/div/div/div[2]/div/div[4]/div/div/div[3]/span'
espera_explicita_element(driver, xpath_activos).click()

# Seleccionar la fecha anterior
seleccionar_fechas('//*[@id="SupermercadosBBRecommercemain-1228722670"]/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div[3]/div/div/div/div/div[2]/div/div/div/div/div/div/div[1]/div/div[1]/div/div/div/div[4]/div/div/div[1]/div/div[3]/div/div[1]/div/div[3]/div/button', 1)

xpath_generar = '//*[@id="SupermercadosBBRecommercemain-1228722670"]/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div[3]/div/div/div/div/div[2]/div/div/div/div/div/div/div[1]/div/div[1]/div/div/div/div[5]/div/div/div'
espera_explicita_element(driver, xpath_generar).click()

time.sleep(15)

boton_descarga(
    '//*[@id="SupermercadosBBRecommercemain-1228722670-overlays"]/div[2]/div/div/div[2]/div')

# Descarga y descomprime archivo zip de Stock
unzip_doc('//*[@id="SupermercadosBBRecommercemain-1228722670-overlays"]/div[3]/div/div/div[3]/div/div/div[3]/div/div[1]',
          'stock', 'stock_supesa.csv')

boton_descarga(
    '//*[@id="SupermercadosBBRecommercemain-1228722670-overlays"]/div[2]/div/div/div[3]')

# Seleccionar 5 días antes
seleccionar_fechas(
    '//*[@id="SupermercadosBBRecommercemain-1228722670-overlays"]/div[3]/div/div/div[3]/div/div/div/div/div/div/div/div[3]/div/div[3]/div/div[3]/div/div/div/button', 5)

# Descarga y descomprime archivo zip de Ventas
unzip_doc('//*[@id="SupermercadosBBRecommercemain-1228722670-overlays"]/div[3]/div/div/div[3]/div/div/div/div/div/div/div/div[9]/div/div/div[1]/div', 'ventas', 'venta_supesa.csv')

cerrar_driver_navegador(driver)
