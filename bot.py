import restricted
import pandas as pd
from selenium_actions import initialize_driver
from get_user_action import get_user_action
from system import System
from modules.Warehouse.product import Product
from modules.Warehouse.registrations import Registrations
from modules.Registrations.neighborhood import Neighborhood

def main():
    url = input("Informe a URL do sistema: ")
    username = restricted.username
    password = restricted.password
    user_action = get_user_action()
    
    driver = initialize_driver()
    system = System(driver)

    try:
        driver.get(url)
        system.login(username, password)
        
        if user_action == '1':
            warehouse_registrations_data = pd.read_csv("almoxarifado_cadastros.csv")
            registrations = Registrations(driver, warehouse_registrations_data)

            warehouse_products_data = pd.read_csv("almoxarifado_produtos.csv")            
            product = Product(driver, warehouse_products_data)

            registrations.register_groups_and_ingredients()
            product.register_all_products()

        elif user_action == '2' or user_action == '3':
            warehouse_products_data = pd.read_csv("almoxarifado_produtos.csv")  
            product = Product(driver, warehouse_products_data)
            product.register_all_products()

        else:
            registrations_neighborhood_data = pd.read_csv("bairros.csv")
            neighborhood = Neighborhood(driver, registrations_neighborhood_data)
            neighborhood.register_neighborhood()

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()