from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def initialize_driver(): 
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized") 
    return webdriver.Chrome(options=chrome_options)

def wait_element_clickable(driver, by_type, selector, timeout=30):
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by_type, selector))
    )

def click_element_add(driver):
    element_add = wait_element_clickable(driver, By.XPATH, "//button[@tooltip='Adicionar']")
    driver.execute_script("arguments[0].click();", element_add)

def click_element_save_and_quit(driver):
    element_save_and_quit = wait_element_clickable(driver, By.XPATH, "//button[text()='Salvar e fechar']")
    driver.execute_script("arguments[0].click();", element_save_and_quit)