from selenium import webdriver
from selenium.webdriver.common.by import By
import sqlite3

con = sqlite3.connect("../database.db")


driver = webdriver.Firefox()
driver.get("https://en.wikipedia.org/wiki/List_of_aircraft_type_designators")

cur = con.cursor()

table = driver.find_elements(By.XPATH, "/html/body/div[3]/div[3]/div[5]/div[1]/table/tbody/tr")
for row in table:
    items = row.find_elements(By.TAG_NAME, 'td')
    if not items:
        continue
    icao = items[0].text
    iata = items[1].text
    model = items[2].text

    cur.execute(
        "insert into aircraft(model, icao, iata) values (?, ?, ?)",
        (model, icao, iata),
    )

driver.close()

con.commit()
con.close()
