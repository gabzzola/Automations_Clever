from selenium.webdriver.common.by import By
from selenium_actions import wait_element_clickable

class Warehouse:
    def __init__(self, driver):
        self.driver = driver 
    
    def click_element_warehouse(self):
        element_warehouse = wait_element_clickable(self.driver, By.CSS_SELECTOR, ".fa.fa-lg.fa-fw.fa-cubes")
        element_warehouse.click()