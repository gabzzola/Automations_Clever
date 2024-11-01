import re
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from modules.Warehouse.main import Warehouse
from selenium_actions import wait_element_clickable, click_element_add, click_element_save_and_quit
from formations import format_price

class Product(Warehouse):
    def __init__(self, driver, dataframe):
        super().__init__(driver)
        self.dataframe = dataframe

    def click_element_products(self):
        element_products = wait_element_clickable(self.driver, By.CSS_SELECTOR, "a[href='#/estoque/produtos']")
        element_products.click()

    def register_all_products(self):
        self.click_element_warehouse()
        self.click_element_products()

        for row in self.dataframe.itertuples():
            self.register_product(row)

    def register_product(self, row):
        click_element_add(self.driver)
        
        product_details = ProductDetails(self.driver, self.dataframe)
        product_details.register_product_details(row)

        product_order_data = ProductOrderData(self.driver, self.dataframe)
        product_order_data.register_product_order_data(row)

        click_element_save_and_quit(self.driver)

    def fill_select(self, selector, row_column):
        element = wait_element_clickable(self.driver, By.CSS_SELECTOR, selector)

        if not pd.isna(row_column):
            item_formatted = row_column.upper()
            
            element.click()
            element.send_keys(item_formatted)

            try:
                option = wait_element_clickable(self.driver, By.XPATH, f"//div[text()='{row_column}']")
                option.click()
            except Exception as e:
                print(f"Erro ao clicar na opção: {e}") 

class ProductDetails(Product):
    def register_product_details(self, row):
        self.code(row)
        self.description(row)
        self.observations(row)
        self.price(row)
        self.delivery_group(row)

    def code(self, row):
        element_code = wait_element_clickable(self.driver, By.ID, "codigo")
        
        if not pd.isna(row.codigo) and isinstance(row.codigo, int):
            element_code.click()
            element_code.send_keys(row.codigo)
    
    def description(self, row):
        element_description = self.driver.find_element(By.ID, "descricao")
        element_description.click()

        description = row.descricao_produto
        description_formatted = description.upper()
        
        element_description.send_keys(description_formatted)

    def observations(self, row):
        element_observations = self.driver.find_element(By.ID, "observacoes")

        if not pd.isna(row.observacoes):
            element_observations.click()
            element_observations.send_keys(str(row.observacoes))

    def price(self, row):
        element_price = self.driver.find_element(By.ID, "valor")

        if not pd.isna(row.valor_de_venda):
            price_formatted = format_price(row.valor_de_venda)

            element_price.click()
            element_price.send_keys(price_formatted)
    
    def delivery_group(self, row):
        self.fill_select("#s2id_grupo_produto_id a.select2-choice.select2-default", row.grupo_delivery)

class ProductOrderData(Product):
    def register_product_order_data(self, row):
        self.click_element_order_data()
        self.order_terminal(row)
        self.delivery_terminal(row)
        self.item_group_and_ingredient(row)

    def click_element_order_data(self):
        element_order_data = wait_element_clickable(self.driver, By.CSS_SELECTOR, "li[active='tabComanda'] a")
        self.driver.execute_script("arguments[0].click();", element_order_data)
    
    def click_element_add_inside_order_data(self):
        element_add = wait_element_clickable(self.driver, By.CSS_SELECTOR, ".btn.btn-cl.btn-info.btn-xs.btn-block.ng-scope")
        self.driver.execute_script("arguments[0].click();", element_add)

    def order_terminal(self, row):
        self.fill_select("#s2id_terminal_id a.select2-choice.select2-default", row.terminal_comanda)
    
    def delivery_terminal(self, row):
        self.fill_select("#s2id_delivery_terminal_id a.select2-choice.select2-default", row.terminal_delivery)

    def item_group_and_ingredient(self, row):
        item_group = row.grupo_item
        ingredient = row.insumo

        if not pd.isna(item_group) and not pd.isna(ingredient):
            group_formatted = re.sub(r"\s*,\s*", ",", item_group)
            ingredient_formatted = re.sub(r"\s*,\s*", ",", ingredient)
            
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
                        item_group_formatted = item_group.upper()
                        element_item_group.select_by_visible_text(item_group_formatted)

                    if wait_element_clickable(self.driver, By.CSS_SELECTOR, "[id^='s2id_produto_id_insumo'] a.select2-choice.select2-default"):
                        ingredient_formatted = ingredient.upper()

                        element_ingredient.click()
                        element_ingredient.send_keys(ingredient_formatted)
                        
                        try:
                            option = wait_element_clickable(self.driver, By.XPATH, f"//div[text()='{ingredient_formatted}']")
                            option.click()

                        except Exception as e:
                            print(f"Erro ao clicar na opção: {e}")