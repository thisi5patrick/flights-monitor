from selenium import webdriver
from selenium.webdriver.common.by import By
import json

driver = webdriver.Firefox()
driver.get("https://en.wikipedia.org/wiki/List_of_aircraft_type_designators")

for i in range(2, 378):
    item = driver.find_element(
        By.XPATH, f"/html/body/div[3]/div[3]/div[5]/div[1]/table/tbody/tr[{i}]"
    ).text
    text = item.split(" ")
    icao = text[0]
    iata = text[1]
    plane = " ".join(text[2:])
    final = {icao: {"iata": iata, "plane_name": plane}}
    string = json.dumps(final)
    string = string.replace("}}", ",}}")
    string += ","

    with open("../constants/plane_icao_codes.py", "a") as f:
        f.write(string)
