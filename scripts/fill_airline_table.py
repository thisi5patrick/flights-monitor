from selenium import webdriver
from selenium.webdriver.common.by import By
import sqlite3
import time

con = sqlite3.connect("../database.db")

driver = webdriver.Firefox()
driver.get("https://en.wikipedia.org/wiki/List_of_airline_codes")
time.sleep(2)

cur = con.cursor()

for i in range(1, 6294):
    icao = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table/tbody/tr[{i}]/td[2]').text
    if not icao:
        continue

    airline = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table/tbody/tr[{i}]/td[3]').text
    call_sign = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table/tbody/tr[{i}]/td[4]').text
    country = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table/tbody/tr[{i}]/td[5]').text

    country_id = cur.execute('select id from country where long_name like (?)', (country,)).fetchone()

    if country_id is None:
        continue

    country_id = country_id[0]

    cur.execute(
        "insert into airline(long_name, call_sign, icao, country_id) values (?, ?, ?, ?)",
        (airline, call_sign, icao, country_id),
    )


driver.close()

con.commit()
con.close()