from selenium import webdriver
from selenium.webdriver.common.by import By
import sqlite3

con = sqlite3.connect("../database.db")


driver = webdriver.Firefox()
driver.get("https://en.wikipedia.org/wiki/List_of_aircraft_type_designators")

cur = con.cursor()

for i in range(3, 249):
    icao = driver.find_element(
        By.XPATH,
        f"/html/body/div[3]/div[3]/div[5]/div[1]/table/tbody/tr[{i}]/td[1]",
    ).text
    iata = driver.find_element(
        By.XPATH,
        f"/html/body/div[3]/div[3]/div[5]/div[1]/table/tbody/tr[{i}]/td[2]",
    ).text
    model = driver.find_element(
        By.XPATH,
        f"/html/body/div[3]/div[3]/div[5]/div[1]/table/tbody/tr[{i}]/td[3]",
    ).text

    cur.execute(
        "insert into aircraft(model, icao, iata) values (?, ?, ?)",
        (model, icao, iata),
    )

driver.close()

con.commit()
con.close()
