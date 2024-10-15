from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from functions import wait_element

class System:
    def __init__(self, driver):
        self.driver = driver

    def login(self, username, password):
        input_username = wait_element(self.driver, By.CSS_SELECTOR, "input[placeholder='Usuário']")
        input_username.clear()
        input_username.send_keys(username + Keys.TAB)
        
        input_password = self.driver.switch_to.active_element
        input_password.send_keys(password + Keys.TAB)
        
        button_login = self.driver.switch_to.active_element
        button_login.send_keys(Keys.ENTER)