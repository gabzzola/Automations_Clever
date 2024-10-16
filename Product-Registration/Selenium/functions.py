from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def initialize_driver(): 
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized") 
    return webdriver.Chrome(options=chrome_options)

def wait_element(driver, by_type, selector, timeout=30):
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((by_type, selector))
    )

def find_add(driver):
    add = wait_element(driver, By.XPATH, "//button[@tooltip='Adicionar']")
    add.click()

def find_save_and_quit(driver):
    save_and_quit = wait_element(driver, By.XPATH, "//button[text()='Salvar e fechar']")
    save_and_quit.click()

def format_price(price):
    price = float(price.replace(',', '.'))
    return f'{price:.2f}'.replace('.', ',')