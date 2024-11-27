import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from modules.Registrations.main import Registrations
from selenium_actions import wait_element_clickable, click_element_add, click_element_save_and_quit
from formations import format_price

class Neighborhood(Registrations):
    def __init__(self, driver, dataframe):
        super().__init__(driver)
        self.dataframe = dataframe

    def click_element_neighborhood(self):
        element_neighborhood = wait_element_clickable(self.driver, By.CSS_SELECTOR, "a[href='#/cliente/bairro']")
        element_neighborhood.click()

    def register_neighborhood(self):
        self.click_element_registrations()
        self.click_element_neighborhood()

        for row in self.dataframe.itertuples():
            neighborhood = row.descricao_bairro
            price = row.valor_motoboy
            city = row.cidade

            if not pd.isna(neighborhood):
                neighborhood_formatted = neighborhood.upper()

                click_element_add(self.driver)
                element_description = wait_element_clickable(self.driver, By.ID, "descricao")
                element_description.click()
                element_description.send_keys(neighborhood_formatted)

                element_show_delivery = self.driver.find_element(By.CSS_SELECTOR, "label[class='onoffswitch-label']")
                element_show_delivery.click()

                if not pd.isna(price):
                    price_formatted = format_price(price)

                    element_price = self.driver.find_element(By.CSS_SELECTOR, "input[placeholder='Valor MotoBoy']")
                    element_price.send_keys(price_formatted)
                
                if not pd.isna(city):
                    city_formatted = (city.upper()) + " - RS"

                    element_city = self.driver.find_element(By.CSS_SELECTOR, "#s2id_cidade_id a.select2-choice.select2-default")
                    element_city.click()

                    input_search = wait_element_clickable(self.driver, By.CSS_SELECTOR, "input.select2-input.select2-focused")
                    input_search.send_keys(city)
                    
                    try:
                        option = wait_element_clickable(self.driver, By.XPATH, f"//div[text()='{city_formatted}']")
                        option.click()

                    except Exception as e:
                        print(f"Erro ao clicar na opção: {e}")

                click_element_save_and_quit(self.driver)