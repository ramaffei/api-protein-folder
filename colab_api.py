from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as ec
import time
import os
import undetected_chromedriver as uc
import pickle

def iniciar_driver():
    options = uc.ChromeOptions()
    options.add_argument("--password-store=basic")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-notifications")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--no-sandbox")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--no-defualt-browser-check")
    options.add_argument("--no-first-run")
    options.add_argument("--no-proxy-server")
    options.add_argument("--disable-blink-features=AutomationControlled")

    options.add_experimental_option(
        "prefs",
        {
            "credentials_enable_service": False,
            "profile.password_manager_enabled:": False,
            "profile.default_content_setting_values.notifications": 2,
            "intl.accept_languages": ["es-ES", "es"]
        }
    )

    driver = uc.Chrome(
        options=options,
        headless=False,
        log_level=3
        )
    
    return driver

def login_driver(driver: uc.Chrome):
    wait = WebDriverWait(driver, 30)
    
    if os.path.isfile("google.cookies"):
        driver.get('https://myaccount.google.com/robots.txt')
        cookies = pickle.load(open("google.cookies", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
        try:
            driver.get("https://myaccount.google.com/")
            e = wait.until(ec.element_to_be_clickable((By.XPATH, "//*[contains(@aria-label,'Rodrigo')]")))
            print('Logueado con exito')
            return driver
        except NoSuchElementException: 
            pass
       
    url_login = "https://accounts.google.com/"
    driver.get(url_login)

    e = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "input[type='email']")))
    e.send_keys('rodrigo.maffei@ipem298.com.ar')
    e.send_keys(Keys.ENTER)

    e = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "input[type='password']")))
    e.send_keys('52866Jam')
    e.send_keys(Keys.ENTER)
    try:
        e = wait.until(ec.element_to_be_clickable((By.XPATH, "//*[contains(@aria-label,'Rodrigo')]")))
        print('Logueado con exito')
    except NoSuchElementException: 
        raise "No se pudo loguear"
    cookies = driver.get_cookies()

    pickle.dump(cookies, open("google.cookies", "wb"))
    print('Cookies guardadas')
    return driver

def ejecutar_colab(driver):
    url_colab = "https://colab.research.google.com/drive/1J6YKItpxrwf9CptWcum9UjDk3S8Cjrjn#scrollTo=toprhYa3NmXt"
    wait = WebDriverWait(driver, 30)
    driver.get(url_colab)
    e = wait.until(ec.element_to_be_clickable((By.CLASS_NAME, "notebook-container")))
    e.click()
    e.send_keys(Keys.CONTROL + Keys.F9)
    
if __name__ == '__main__':
    driver = iniciar_driver()
    login_driver(driver)
    ejecutar_colab(driver)
    input('Programa Terminado, presiona una tecla para salir')
    driver.quit()