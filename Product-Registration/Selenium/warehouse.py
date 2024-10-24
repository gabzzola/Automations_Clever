import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium_actions import wait_element_clickable, click_element_add, click_element_save_and_quit
from formations import format_price

class Warehouse:
    def __init__(self, driver):
        self.driver = driver 
    
    def click_element_warehouse(self):
        element_warehouse = wait_element_clickable(self.driver, By.CSS_SELECTOR, ".fa.fa-lg.fa-fw.fa-cubes")
        element_warehouse.click()

class Registrations(Warehouse):
    def __init__(self, driver, warehouse_registrations_data):
        super().__init__(driver)
        self.warehouse_registrations_data = warehouse_registrations_data

    def click_element_registrations(self):
        element_registrations = wait_element_clickable(self.driver, By.XPATH, "//span[contains(text(), 'Almoxarifado')]/ancestor::li//span[contains(text(), 'Cadastros')]")
        element_registrations.click()

    def click_element_delivery_group(self):
        element_delivery_group = wait_element_clickable(self.driver, By.CSS_SELECTOR, "a[href='#/estoque/grupos']")
        element_delivery_group.click()

    def click_element_item_group(self):
        element_item_group = wait_element_clickable(self.driver, By.CSS_SELECTOR, "a[href='#/estoque/grupo_item']")
        element_item_group.click()

    def click_element_ingredients(self):
        element_ingredients = wait_element_clickable(self.driver, By.CSS_SELECTOR, "a[href='#/estoque/insumos']")
        element_ingredients.click()

    def register_delivery_groups(self):
        self.click_element_warehouse()
        self.click_element_registrations()
        self.click_element_delivery_group()
        self.logic_register_groups(self.warehouse_registrations_data, "grupo_delivery")

    def register_item_groups(self):
        self.click_element_warehouse()
        self.click_element_registrations()
        self.click_element_item_group()
        self.logic_register_groups(self.warehouse_registrations_data, "grupo_item")

    def register_ingredients(self):
        self.click_element_warehouse()
        self.click_element_registrations()
        self.click_element_ingredients()

        for row in self.warehouse_registrations_data.itertuples():
            ingredient = row.insumo
            price = row.valor_insumo
            
            if not pd.isna(ingredient): 
                time.sleep(1)
                click_element_add(self.driver)
                ingredient_formatted = ingredient.upper()
                element_description = wait_element_clickable(self.driver, By.ID, "descricao")
                element_description.send_keys(ingredient_formatted + Keys.TAB)

                if not pd.isna(price):
                    price_formatted = format_price(price)
                    element_price = self.driver.switch_to.active_element
                    element_price.send_keys(price_formatted)
                
                click_element_save_and_quit(self.driver)

    def logic_register_groups(self, df, column_item):
        registered_items = set()
        for row in df.itertuples():
            item = getattr(row, column_item)

            if not pd.isna(item) and item not in registered_items:
                time.sleep(1)
                click_element_add(self.driver)
                element_description = wait_element_clickable(self.driver, By.ID, "descricao")
                element_description.send_keys(item)
                click_element_save_and_quit(self.driver)

                registered_items.add(item)

class Product(Warehouse):
    def __init__(self, driver, warehouse_products_data):
        super().__init__(driver)
        self.warehouse_products_data = warehouse_products_data

    def click_element_products(self):
        element_products = wait_element_clickable(self.driver, By.CSS_SELECTOR, "a[href='#/estoque/produtos']")
        element_products.click()

    def click_element_order_data(self):
        element_order_data = wait_element_clickable(self.driver, By.CSS_SELECTOR, "li[active='tabComanda'] a")
        self.driver.execute_script("arguments[0].click();", element_order_data)
    
    def click_element_add_inside_order_data(self):
        element_add = wait_element_clickable(self.driver, By.CSS_SELECTOR, ".btn.btn-cl.btn-info.btn-xs.btn-block.ng-scope")
        self.driver.execute_script("arguments[0].click();", element_add)

    def register_all_products(self):
        self.click_element_warehouse()
        self.click_element_products()

        for row in self.warehouse_products_data.itertuples():
            self.register_product(row)

    def register_product(self, row):
        time.sleep(1)
        click_element_add(self.driver)
        self.product_module_details(row)
        self.product_module_order_data(row)
        click_element_save_and_quit(self.driver)
    
    def product_module_details(self, row):
        self.code(row)
        self.description(row)
        self.observations(row)
        self.price(row)
        self.delivery_group(row)

    def product_module_order_data(self, row):
        self.click_element_order_data()
        self.order_terminal(row)
        self.delivery_terminal(row)
        self.item_groups_and_ingredients(row)

    def code(self, row):
        element_code = wait_element_clickable(self.driver, By.ID, "codigo")
        element_code.click()
        
        if not pd.isna(row.codigo) and isinstance(row.codigo, int):
            element_code.send_keys(row.codigo)

    def description(self, row):
        element_description = self.driver.find_element(By.ID, "descricao")
        element_description.click()

        if not pd.isna(row.descricao_produto):
            description = row.descricao_produto
            description_formatted = str(description.upper())
            element_description.send_keys(description_formatted)

    def observations(self, row):
        element_observations = self.driver.find_element(By.ID, "observacoes")
        element_observations.click()

        if not pd.isna(row.observacoes):
            element_observations.send_keys(str(row.observacoes))

    def price(self, row):
        element_price = self.driver.find_element(By.ID, "valor")
        element_price.click()

        if not pd.isna(row.valor_de_venda):
            price_formatted = format_price(row.valor_de_venda)
            element_price.send_keys(price_formatted)

    def delivery_group(self, row):
        element_delivery_group = self.driver.find_element(By.CSS_SELECTOR, "#s2id_grupo_produto_id a.select2-choice.select2-default")
        element_delivery_group.click()
        
        if not pd.isna(row.grupo_delivery):
            element_delivery_group.send_keys(row.grupo_delivery)
            try:
                option = wait_element_clickable(self.driver, By.XPATH, f"//div[contains(text(), '{row.grupo_delivery}')]")
                option.click()
            except Exception as e:
                print(f"Erro ao clicar na opção: {e}")

    def order_terminal(self, row):
        element_order_terminal = wait_element_clickable(self.driver, By.CSS_SELECTOR, "#s2id_terminal_id a.select2-choice.select2-default")
        element_order_terminal.click()

        if not pd.isna(row.terminal_comanda):
            order_terminal_formatted = row.terminal_comanda.upper()
            element_order_terminal.send_keys(order_terminal_formatted)
            try:
                option = wait_element_clickable(self.driver, By.XPATH, f"//div[contains(text(), '{order_terminal_formatted}')]")
                option.click()
            except Exception as e:
                print(f"Erro ao clicar na opção: {e}")

    def delivery_terminal(self, row):
        element_delivery_terminal = self.driver.find_element(By.CSS_SELECTOR, "#s2id_delivery_terminal_id a.select2-choice.select2-default")
        element_delivery_terminal.click()

        if not pd.isna(row.terminal_delivery):
            delivery_terminal_formatted = row.terminal_delivery.upper()
            element_delivery_terminal.send_keys(delivery_terminal_formatted)
            try:
                option = wait_element_clickable(self.driver, By.XPATH, f"//div[contains(text(), '{delivery_terminal_formatted}')]")
                option.click()
            except Exception as e:
                print(f"Erro ao clicar na opção: {e}")

    def item_groups_and_ingredients(self, row):
        item_group = row.grupo_item
        ingredient = row.insumo

        if not pd.isna(item_group) and not pd.isna(ingredient):
            group_formatted = item_group.replace(", ", ",")
            ingredient_formatted = ingredient.replace(", ", ",")
            
            array_groups = group_formatted.split(',')
            array_ingredients = ingredient_formatted.split(',')
            
            for item_group, ingredient in zip(array_groups, array_ingredients):
                self.click_element_add_inside_order_data()
                all_elements_item_groups = self.driver.find_elements(By.CSS_SELECTOR, "[id^='grupo_item']")
                all_elements_ingredients = self.driver.find_elements(By.CSS_SELECTOR, "[id^='s2id_produto_id_insumo'] a.select2-choice.select2-default")
                
                if all_elements_item_groups and all_elements_ingredients:
                    last_element_item_group = all_elements_item_groups[-1]
                    last_element_ingredient = all_elements_ingredients[-1]

                    element_item_group = Select(last_element_item_group)
                    element_ingredient = last_element_ingredient

                    if wait_element_clickable(self.driver, By.CSS_SELECTOR, "[id^='grupo_item']"):
                        element_item_group.select_by_visible_text(item_group)

                    if wait_element_clickable(self.driver, By.CSS_SELECTOR, "[id^='s2id_produto_id_insumo'] a.select2-choice.select2-default"):
                        time.sleep(2)
                        element_ingredient.click()
                        ingredient_formatted = str(ingredient.upper())
                        input_search = wait_element_clickable(self.driver, By.CSS_SELECTOR, "input.select2-input.select2-focused")
                        input_search.send_keys(ingredient_formatted)
                        
                        try:
                            option = wait_element_clickable(self.driver, By.XPATH, f"//div[contains(text(), '{ingredient_formatted}')]")
                            option.click()
                        except Exception as e:
                            print(f"Erro ao clicar na opção: {e}")