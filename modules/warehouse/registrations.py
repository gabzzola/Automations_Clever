import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from modules.Warehouse.main import Warehouse
from selenium_actions import wait_element_clickable, click_element_add, click_element_save_and_quit
from formations import format_price

class Registrations(Warehouse):
    def __init__(self, driver, dataframe):
        super().__init__(driver)
        self.dataframe = dataframe

    def click_element_registrations(self):
        element_registrations = wait_element_clickable(self.driver, By.XPATH, "//span[contains(text(), 'Almoxarifado')]/ancestor::li//span[contains(text(), 'Cadastros')]")
        element_registrations.click()

    def register_groups_and_ingredients(self):
        delivery_group = DeliveryGroup(self.driver, self.dataframe)
        delivery_group.register_delivery_groups()

        item_group = ItemGroup(self.driver, self.dataframe)
        item_group.register_item_groups()

        ingredient = Ingredients(self.driver, self.dataframe)
        ingredient.register_ingredients()

    def logic_register_groups(self, dataframe, column_item):
        registered_items = set()
        for row in dataframe.itertuples():
            item = getattr(row, column_item)

            if not pd.isna(item) and item not in registered_items:
                item_formatted = item.upper()
                
                click_element_add(self.driver)
                element_description = wait_element_clickable(self.driver, By.ID, "descricao")
                element_description.send_keys(item_formatted)
                click_element_save_and_quit(self.driver)

                registered_items.add(item)

class DeliveryGroup(Registrations):
    def click_element_delivery_group(self):
        element_delivery_group = wait_element_clickable(self.driver, By.CSS_SELECTOR, "a[href='#/estoque/grupos']")
        element_delivery_group.click()
    
    def register_delivery_groups(self):
        self.click_element_warehouse()
        self.click_element_registrations()
        self.click_element_delivery_group()
        self.logic_register_groups(self.dataframe, "grupo_delivery")

class ItemGroup(Registrations):
    def click_element_item_group(self):
        element_item_group = wait_element_clickable(self.driver, By.CSS_SELECTOR, "a[href='#/estoque/grupo_item']")
        element_item_group.click()

    def register_item_groups(self):
        self.click_element_warehouse()
        self.click_element_registrations()
        self.click_element_item_group()
        self.logic_register_groups(self.dataframe, "grupo_item")

class Ingredients(Registrations):
    def click_element_ingredients(self):
        element_ingredients = wait_element_clickable(self.driver, By.CSS_SELECTOR, "a[href='#/estoque/insumos']")
        element_ingredients.click()

    def register_ingredients(self):
        self.click_element_warehouse()
        self.click_element_registrations()
        self.click_element_ingredients()

        for row in self.dataframe.itertuples():
            ingredient = row.insumo
            price = row.valor_insumo
            
            if not pd.isna(ingredient): 
                ingredient_formatted = ingredient.upper()

                click_element_add(self.driver)
                element_description = wait_element_clickable(self.driver, By.ID, "descricao")
                element_description.send_keys(ingredient_formatted + Keys.TAB)

                if not pd.isna(price):
                    price_formatted = format_price(price)
                    element_price = self.driver.switch_to.active_element
                    element_price.send_keys(price_formatted)
                
                click_element_save_and_quit(self.driver)