import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from functions import wait_element, find_add, find_save_and_quit, format_price

warehouse_registrations_data = pd.read_csv("C:/Users/gazzo/OneDrive/Documents/GitHub/Automations_Python/Product-Registration/Selenium/database/almoxarifado_cadastros.csv")
print(warehouse_registrations_data)

class Warehouse:
    def __init__(self, driver):
        self.driver = driver 
    
    def localize_warehouse(self):
        warehouse = wait_element(self.driver, By.CSS_SELECTOR, ".fa.fa-lg.fa-fw.fa-cubes")
        warehouse.click()

class Registrations(Warehouse):
    def localize_registrations(self):
        registrations = wait_element(self.driver, By.XPATH, "//span[contains(text(), 'Almoxarifado')]/ancestor::li//span[contains(text(), 'Cadastros')]")
        registrations.click()
    
    def localize_delivery_group(self):
        delivery_group = wait_element(self.driver, By.CSS_SELECTOR, "a[href='#/estoque/grupos']")
        delivery_group.click()

    def localize_item_group(self):
        item_group = wait_element(self.driver, By.CSS_SELECTOR, "a[href='#/estoque/grupo_item']")
        item_group.click()

    def localize_ingredients(self):
        ingredients = wait_element(self.driver, By.CSS_SELECTOR, "a[href='#/estoque/insumos']")
        ingredients.click()

    def register_delivery_group(self):
        self.localize_warehouse()
        self.localize_registrations()
        self.localize_delivery_group()

        registered_groups = set()

        for row in warehouse_registrations_data.itertuples():
            delivery_group = row.grupo_delivery

            if not pd.isna(delivery_group) and delivery_group not in registered_groups:
                time.sleep(1)
                find_add(self.driver)
                description = wait_element(self.driver, By.ID, "descricao")
                description.send_keys(delivery_group)
                find_save_and_quit(self.driver)

    def register_item_group(self):
        self.localize_warehouse()
        self.localize_registrations()
        self.localize_item_group()

        registered_groups = set()

        for row in warehouse_registrations_data.itertuples():
            item_group = row.grupo_item
            
            if not pd.isna(item_group) and item_group not in registered_groups:
                time.sleep(1)
                find_add(self.driver)        
                description = wait_element(self.driver, By.ID, "descricao")
                description.send_keys(item_group)
                find_save_and_quit(self.driver)
                
                registered_groups.add(item_group)
    
    def register_ingredients(self):
        self.localize_warehouse()
        self.localize_registrations()
        self.localize_ingredients()

        for row in warehouse_registrations_data.itertuples():
            ingredients = row.insumo
            price = row.valor_insumo
            
            if ingredients:
                time.sleep(1)
                find_add(self.driver)
                ingredients_formatted = ingredients.upper()
                description = wait_element(self.driver, By.ID, "descricao")
                description.send_keys(ingredients_formatted + Keys.TAB)

                if price:
                    price_formatted = format_price(price)
                    price = self.driver.switch_to.active_element
                    price.send_keys(price_formatted)
                find_save_and_quit(self.driver)

class Products(Warehouse):
    def localize_products(self):
        products = wait_element(self.driver, By.CSS_SELECTOR, "a[href='#/estoque/produtos']")
        products.click()