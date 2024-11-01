from selenium.webdriver.common.by import By
from selenium_actions import wait_element_clickable

class Registrations:
    def __init__(self, driver):
        self.driver = driver

    def click_element_registrations(self):
        element_registrations = wait_element_clickable(self.driver, By.CSS_SELECTOR, ".fa.fa-lg.fa-fw.fa-gears")
        element_registrations.click()