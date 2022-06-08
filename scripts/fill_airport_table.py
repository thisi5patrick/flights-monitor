from selenium import webdriver
from selenium.webdriver.common.by import By
import sqlite3

con = sqlite3.connect("../database.db")


driver = webdriver.Firefox()
driver.minimize_window()
driver.get("http://www.flugzeuginfo.net/table_airportcodes_country-location_en.php#startanker")

cur = con.cursor()

parts = driver.find_elements(By.XPATH, '/html/body/main/div/div/section[2]/article/div/table')

country_standarization = {
    'USA': 'UNITED STATES OF AMERICA',
    'Aruba (Netherlands)': 'ARUBA',
    'Bosnia-Hercegovina': 'BOSNIA AND HERZEGOVINA',
    'Central Africa': 'CENTRAL AFRICAN REPUBLIC',
    'China - Peoples Republic': 'PEOPLE’S REPUBLIC OF CHINA',
    'Congo, Democratic Republic of the': 'CONGO (DEMOCRATIC REPUBLIC)',
    'Congo, Republic of': 'CONGO',
    'East Timor (Timor-Leste)': 'EAST TIMOR',
    'Falkland Islands (UK)': 'FALKLAND ISLANDS',
    'Faroe Islands (Denmark)': 'FAROE ISLANDS',
    'Gibraltar (UK)': 'GIBRALTAR',
    'Greenland (Denmark)': 'GREENLAND',
    'Guadeloupe - French Antilles': 'GUADELOUPE',
    'Guam (USA)': 'GUAM',
    'Guinea Bissau': 'GUINEA-BISSAU',
    'Martinique - French Antilles': 'MARTINIQUE',
    'Micronesia, Federated States of': 'MICRONESIA',
    'Myanmar (Burma)': 'MYANMAR',
    'New Caledonia (France)': 'NEW CALEDONIA',
    'North Korea': "DEMOCRATIC PEOPLE'S REPUBLIC OF KOREA",
    'Russia': 'RUSSIAN FEDERATION',
    'Saint-Pierre and Miquelon': 'SAINT PIERRE AND MIQUELON',
    'South Korea': 'REPUBLIC OF KOREA',
    'St. Vincent & Grenadines': 'SAINT VINCENT AND THE GRENADINES',
    'Taiwan, Republic of China': 'TAIWAN',
    'Trinidad & Tobago': 'TRINIDAD AND TOBAGO',
    'Turks & Caicos': 'TURKS AND CAICOS ISLANDS',
    'Argentina': 'ARGENTINA REPUBLIC',
    'Iran': 'ISLAMIC REPUBLIC OF IRAN',
    'Syria': 'SYRIAN ARAB REPUBLIC',
    'Tanzania': 'UNITED REPUBLIC OF TANZANIA',
    'Botsuana': 'BOTSWANA',
    'Tunesia': 'TUNISIA'
}

not_present = set()

for part in parts:
    lines = part.find_elements(By.TAG_NAME, 'tr')
    lines.pop(0)
    for line in lines:
        line = line.find_elements(By.TAG_NAME, 'td')
        iata = line[0].text
        icao = line[1].text
        location = line[2].text
        airport_name = line[3].text
        country = line[4].text
        if country in country_standarization:
            country = country_standarization[country]
        country_id = con.execute('select id from country where long_name like (?)', (country,)).fetchone()
        if not country_id:
            not_present.add(country)
            continue
        country_id = country_id[0]
        con.execute('insert into airport(name, icao, country_id, iata, location) values (?,?,?,?,?)',
                    (airport_name, icao, country_id, iata, location))

driver.close()

con.commit()
con.close()
