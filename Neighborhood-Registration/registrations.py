import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium_actions import wait_element_clickable, click_element_add, click_element_save_and_quit
from formations import format_price

class Registrations:
    def __init__(self, driver):
        self.driver = driver

    def click_element_registrations(self):
        element_registrations = wait_element_clickable(self.driver, By.CSS_SELECTOR, ".fa.fa-lg.fa-fw.fa-gears")
        element_registrations.click()

class Neighborhood(Registrations):
    def __init__(self, driver, registrations_neighborhood_data):
        super().__init__(driver)
        self.registrations_neighborhood_data = registrations_neighborhood_data

    def click_element_neighborhood(self):
        element_neighborhood = wait_element_clickable(self.driver, By.CSS_SELECTOR, "a[href='#/cliente/bairro']")
        element_neighborhood.click()

    def register_neighborhood(self):
        self.click_element_registrations()
        self.click_element_neighborhood()

        for row in self.registrations_neighborhood_data.itertuples():
            neighborhood = row.descricao_bairro
            price = row.valor_motoboy

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
                
                click_element_save_and_quit(self.driver)