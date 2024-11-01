from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium_actions import wait_element_clickable

class System:
    def __init__(self, driver):
        self.driver = driver

    def login(self, username, password):
        element_username = wait_element_clickable(self.driver, By.CSS_SELECTOR, "input[placeholder='Usuário']")
        element_username.clear()
        element_username.send_keys(username + Keys.TAB)
        
        element_password = self.driver.switch_to.active_element
        element_password.send_keys(password + Keys.TAB)
        
        element_login = self.driver.switch_to.active_element
        element_login.send_keys(Keys.ENTER)