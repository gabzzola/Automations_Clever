import time
import restricted
import pandas as pd
from selenium_actions import initialize_driver
from system import System
from warehouse import Registrations, Product

"""
url = input("Informe a URL do sistema: ")
username = input("Informe o usuário de acesso ao sistema: ")
password = input("Informe a senha: ")
"""

def main():
    url = restricted.url
    username = restricted.username
    password = restricted.password
    
    warehouse_registrations_data = pd.read_csv("C:/Users/gazzo/OneDrive/Documents/GitHub/Automations_Python/Product-Registration/Selenium/database/registrations_header.csv")
    warehouse_products_data = pd.read_csv("C:/Users/gazzo/OneDrive/Documents/GitHub/Automations_Python/Product-Registration/Selenium/database/products_header.csv")

    driver = initialize_driver()
    system = System(driver)
    registrations = Registrations(driver, warehouse_registrations_data)
    product = Product(driver, warehouse_products_data)

    try:
        driver.get(url)
        system.login(username, password)
        
        registrations.register_delivery_groups()
        registrations.register_item_groups()
        registrations.register_ingredients()    
        
        product.register_all_products()
        
        time.sleep(5)

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        driver.close()

if __name__ == "__main__":
    main()