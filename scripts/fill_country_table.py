import sqlite3

from selenium import webdriver
from selenium.webdriver.common.by import By

con = sqlite3.connect("../database.db")


driver = webdriver.Firefox()
driver.get("https://sustainablesources.com/resources/country-abbreviations/")

cur = con.cursor()

table = driver.find_elements(By.XPATH, "/html/body/div/div/div/div[1]/div/article/div/div/div/div[3]/figure/table/tbody/tr")

for row in table:
    items = row.find_elements(By.TAG_NAME, "td")
    if not items:
        continue
    country_long_name = items[0].text
    country_short_name = items[1].text

    cur.execute(
        "insert into country(long_name, short_name) values (?, ?)",
        (country_long_name, country_short_name),
    )

driver.close()

con.commit()
con.close()
