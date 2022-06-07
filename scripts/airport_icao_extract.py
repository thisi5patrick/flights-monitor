from selenium import webdriver
from selenium.webdriver.common.by import By
import json

driver = webdriver.Firefox()
driver.get("https://airmundo.com/en/blog/airport-codes-european-airports/")

for i in range(1, 265):
    airport_name = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/main/div[3]/div/article/div[1]/div/div/table/tbody/tr[{i}]/td[1]').text
    country = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/main/div[3]/div/article/div[1]/div/div/table/tbody/tr[{i}]/td[2]').text
    iata = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/main/div[3]/div/article/div[1]/div/div/table/tbody/tr[{i}]/td[3]').text
    icao = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/main/div[3]/div/article/div[1]/div/div/table/tbody/tr[{i}]/td[4]').text

    item = {
        icao: {
            "iata_code": iata,
            "airport_name": airport_name,
            "country": country
        }
    }

    string = json.dumps(item)
    string = string.replace("}}", ",}}")
    string += ","

    with open("../constants/airport_icao_codes.py", "a") as f:
        f.write(string)

driver.close()
