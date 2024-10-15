import time
import restricted
from functions import initialize_driver
from system import System
from warehouse import Registrations

"""
url = input("Informe a URL do sistema: ")
username = input("Informe o usuário de acesso ao sistema: ")
password = input("Informe a senha: ")
"""

def main():
    url = restricted.url
    username = restricted.username
    password = restricted.password

    driver = initialize_driver()
    system = System(driver)
    registrations = Registrations(driver)

    try:
        driver.get(url)
        system.login(username, password)

        registrations.register_delivery_group()

        registrations.register_item_group()

        registrations.register_ingredients()    
    
        time.sleep(15)

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        driver.close()

if __name__ == "__main__":
    main()