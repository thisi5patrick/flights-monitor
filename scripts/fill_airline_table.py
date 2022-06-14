"""
This file fills the airline table from the planespotters.net site.
A selenium web-scrapper is initialized which will go through each letter and each page of the
letter to extract the airlines and their ICAO codes. Only airlines with > 0 aircrafts will be saved.
Since the site allows only around 450 requests per 24 hours, 3 users must be created (or wait 24
hours to extract the second half of airlines).
All extracted airlines are saved into the txt_files/visited.txt file to keep track which airlines have been extracted.
After the second user is initialized this way, no new requests will be created and the extraction will continue
from the last extracted airline.
The site has a lot of popup adds, so an Adblock has to be added to the driver.
TODO: remove the necessity of adblock

Some countries are not written the same as the countries extracted from the fill_country_table.py file,
hence the COUNTRIES_PARSER dictionary to standardize them.
"""
from typing import Union

from selenium import webdriver
from selenium.webdriver.common.by import By
import sqlite3
import re
import os

COUNTRIES_PARSER = {
    "Moldova, Republic Of": "MOLDOVA",
    "United States": "UNITED STATES OF AMERICA",
    "Türkiye": "TURKEY",
    "Argentina": "ARGENTINA REPUBLIC",
    "Korea, Democratic People's Republic Of": "DEMOCRATIC PEOPLE'S REPUBLIC OF KOREA",
    "Cote d'Ivoire": "COTE D IVOIRE",
    "China": "PEOPLE’S REPUBLIC OF CHINA",
    "Tanzania, United Republic Of": "UNITED REPUBLIC OF TANZANIA",
    "Korea, Republic Of": "REPUBLIC OF KOREA",
    "Iran, Islamic Republic Of": "ISLAMIC REPUBLIC OF IRAN",
    "Czechia": "CZECH REPUBLIC",
    "Viet Nam": "VIETNAM",
    "Lao People's Democratic Republic": "LAO PEOPLE’S DEM. REPUBLIC",
    "Air One Aviation": "ADH",
    "Congo, The Democratic Republic Of The": "CONGO (DEMOCRATIC REPUBLIC)",
}


EMAIL = ""
PASSWORD = ""
AD_BLOCK_PATH = ""


def login_user(driver: webdriver) -> None:
    """
    Function will insert the username/email and password into the proper placeholders.
    Sometimes a CAPTCHA is shown and/or cookie information so the user must manually complete these steps.
    After that the Enter Key must be pressed to continue with the extraction
    :param driver: a webdriver object must be passed.
    :return: None
    """
    driver.get("https://www.planespotters.net/user/login")
    driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(EMAIL)
    driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(PASSWORD)
    input("LOGIN AND PRESS ENTER")


def init_planesspotter_driver() -> webdriver:
    """
    Initializes the webdriver. In this case it is a Firefox webdriver.
    The function also takes the user to the login page to log in.
    After that the user is taken to the main page where the airlines will be extracted
    :return: webdriver object
    """
    driver = webdriver.Firefox(service_log_path=os.devnull)
    driver.install_addon(AD_BLOCK_PATH, temporary=True)
    login_user(driver)
    driver.get("https://www.planespotters.net/airlines")
    return driver


def close(driver: webdriver) -> None:
    """
    Exit program. Close necessary objects
    :param driver: Webdriver element
    :return: None
    """
    driver.quit()
    con.close()
    exit(0)


def get_icao(driver: webdriver, link: str) -> Union[str, None]:
    """
    Extract icao from a given page. If icao not exists return None.
    If limit has been reached the program is terminated
    :param driver: webdriver object
    :param link: link of airline with icao information
    :return:  string of icao or None
    """
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(link)
    try:
        icao = driver.find_element(By.XPATH, "/html/body/main/div/div[1]/div[1]/table/tbody/tr[1]/td[2]/b").text
    except Exception:
        try:
            icao = driver.find_element(By.XPATH, "/html/body/main/div/div[1]/div[1]/table/tbody/tr[2]/td[2]/b").text
        except Exception:
            try:
                driver.find_element(By.XPATH, "/html/body/main/div/h2[1]")
                icao = None
            except Exception:
                print("START THE PROGRAM AGAIN WITH NEW USER OR WAIT 24 HOURS.")
                close(driver)
    driver.execute_script("window.close('');")
    driver.switch_to.window(driver.window_handles[0])
    return icao


def save_visited(link: str) -> None:
    """
    Saves all visited sites.
    Saving it into a txt file gives the possibility to see which airlines have been visited even after a program exit
    :param link: link of the airline
    :return: None
    """
    with open("txt_files/visited.txt", "a+") as f:
        f.write(f"{link}\n")


def save_airline(name: str) -> None:
    """
    Saved airlines which have no available ICAO code in their site
    :param name: airline name
    :return: None
    """
    with open("txt_files/no_icao_airlines.txt", "a+") as f:
        f.write(f"{name}\n")


def save_country(name: str) -> None:
    """
    Saved countries that could not be matched with countries from the countries table
    :param name: country name
    :return: None
    """
    with open("txt_files/country.txt", "a+") as f:
        f.write(f"{name}\n")


def is_country_saved(name: str) -> bool:
    """
    Checks whether a given country have been saved in the country.txt file.
    :param name: country name
    :return: bool object if country is saved
    """
    with open("txt_files/country.txt") as f:
        countries = f.read().split("\n")
    return name in countries


def is_visited(link: str) -> bool:
    """
    Checks if an airline site with a given link has already been visited
    :param link: link to airline
    :return: bool object if airline is already visited
    """
    with open("txt_files/visited.txt") as f:
        lines = f.read().split("\n")
    return link in lines


def extract_data(driver) -> None:
    """
    Extract data from a particular page of a letter.
    Data is saved into the airline table
    :param driver: webdriver object
    :return: None
    """
    rows = driver.find_elements(By.XPATH, "/html/body/main/div[2]/div[3]/div[1]/div/div")
    rows.pop(0)
    for row in rows:
        row = row.find_elements(By.TAG_NAME, "div")
        airline_name = row[1].text
        country = row[2].text
        fleet_num = row[3].text
        if not re.match("\d+", fleet_num):
            continue
        link = row[1].find_element("tag name", "a").get_attribute("href")
        if is_visited(link):
            continue
        icao = get_icao(driver, link)
        save_visited(link)
        if icao is None:
            save_airline(airline_name)
            continue
        if country in COUNTRIES_PARSER:
            country = COUNTRIES_PARSER[country]
        country_id = con.execute("select id from country where long_name like (?)", (country,)).fetchone()
        if not country_id:
            if not is_country_saved(country):
                save_country(country)
            continue
        country_id = country_id[0]
        con.execute(
            "insert into airline(long_name, icao, country_id) values (?, ?, ?)",
            (airline_name, icao, country_id),
        )
        con.commit()


def parse_planesspotter(driver: webdriver) -> None:
    """
    Main function to parse the planesspotter site.
    It loops through every letter in the provided category and in every page of such letter
    :param driver: initialized webdriver
    :return: None
    """
    alphabet = driver.find_elements(By.XPATH, "/html/body/main/div[1]/div/div/a")
    for letter in range(len(alphabet)):
        pages = driver.find_elements(By.XPATH, "(/html/body/main/div[2]/div[1]/div/div[2]/a)[last()]")
        if pages:
            pages = int(pages[0].text)
            for i in range(1, pages + 1):
                extract_data(driver)
                if i != pages:
                    driver.find_element(By.XPATH, "/html/body/main/div[2]/div[1]/div/div[3]/a").click()
        else:
            extract_data(driver)
        if letter != len(alphabet) - 1:
            driver.find_element(
                By.XPATH, "//a[contains(@class, 'letter__index_link_active')]/following-sibling::a[1]"
            ).click()


con = sqlite3.connect("../database.db")

driver = init_planesspotter_driver()

parse_planesspotter(driver)

driver.quit()

con.close()
