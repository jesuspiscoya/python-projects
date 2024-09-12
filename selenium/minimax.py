from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.FirefoxOptions()
options.binary_location = "C:/Program Files/Firefox Developer Edition/firefox.exe"

browser = webdriver.Firefox(options=options)
browser.implicitly_wait(10)
browser.get("https://minimax.laive.pe")

input_user = browser.find_element(By.ID, "NOMUsuario")
input_pass = browser.find_element(By.ID, "password")
input_user.send_keys("ayp27")
input_pass.send_keys("ayp27")
input_pass.submit()

browser.implicitly_wait(10)

browser.find_element(By.LINK_TEXT, "Recomendaciones").click()

browser.implicitly_wait(10)

for i in range(50):
    table_client = browser.find_element(
        By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")

    for index, client in enumerate(table_client):
        if index == 2:
            client.find_element(By.TAG_NAME, "a").click()
            break

    try:
        text_client = browser.find_element(By.TAG_NAME, "strong").text
        print(f"Se encontró el cliente: {text_client}")
    except:
        print("Error con cliente")

    browser.find_element(By.TAG_NAME, "a").click()
