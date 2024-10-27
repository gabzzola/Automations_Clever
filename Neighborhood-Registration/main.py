import time
import restricted
import pandas as pd
from selenium_actions import inicialize_driver
from system import System
from registrations import Neighborhood

def main():
    registrations_neighborhood_data = pd.read_csv("C:/Users/gazzo/OneDrive/Documents/GitHub/Automations_Python/Neighborhood-Registration/database/neighborhood_header.csv")

    url = restricted.url
    username = restricted.username
    password = restricted.password

    driver = inicialize_driver()
    system = System(driver)
    neighborhood = Neighborhood(driver, registrations_neighborhood_data)

    try:
        driver.get(url)
        system.login(username, password)

        neighborhood.register_neighborhood()

        time.sleep(10)

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

    finally:
        driver.close()

if __name__ == '__main__':
    main()