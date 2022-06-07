from selenium import webdriver
from selenium.webdriver.common.by import By
import sqlite3

con = sqlite3.connect("../database.db")


driver = webdriver.Firefox()
driver.get("https://sustainablesources.com/resources/country-abbreviations/")

cur = con.cursor()

for i in range(3, 249):
    country_long_name = driver.find_element(
        By.XPATH,
        f"/html/body/div/div/div/div[1]/div/article/div/div/div/div[3]/figure/table/tbody/tr[{i}]/td[1]",
    ).text
    country_short_name = driver.find_element(
        By.XPATH,
        f"/html/body/div/div/div/div[1]/div/article/div/div/div/div[3]/figure/table/tbody/tr[{i}]/td[2]",
    ).text

    cur.execute(
        "insert into country(long_name, short_name) values (?, ?)",
        (country_long_name, country_short_name),
    )

driver.close()

con.commit()
con.close()
