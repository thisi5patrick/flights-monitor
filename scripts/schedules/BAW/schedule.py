from datetime import date, timedelta
from requests_html import HTMLSession

import requests
from lxml import html

DESTINATIONS_URL = "https://www.britishairways.com/en-pl/information/flight-information/our-route-network"
URL = "https://www.britishairways.com/travel/schedules/public/en_pl"

# TODO it should be a selenium scrapper?

PARAMS = {
    "eid": "116001",
    "depDay": "",
    "depMonth": "",
    "retDay": "",
    "retMonth": "",
    "from-full": "",
    "from": "",
    "to-full": "",
    "to": "",
    "showReturnOption": "True",
    "display": "Display+flights",
}

HEADERS = {"User-Agent": "None"}


def get_destinations() -> list:
    response = requests.get(DESTINATIONS_URL, headers=HEADERS)
    tree = html.fromstring(response.text)
    destinations_list = []
    destinations = tree.xpath("//span[@class='routesListCode']")
    for destination in destinations:
        destinations_list.append(destination.text_content().strip().replace("(", "").replace(")", ""))
    return list(set(destinations_list))


def get_iata_full_parameter(airport_iata) -> str:
    response = requests.get(
        f"https://www.britishairways.com/dwr/exec/locationHelper.getMatchedLocations.dwr?callCount=1&c0-scriptName=locationHelper&c0-methodName=getMatchedLocations&xml=true&c0-param0=string:{airport_iata}",
        headers=HEADERS,
    ).text
    response = response.split(";")
    for line in response:
        line_split = line.split(",")
        try:
            line_iata = line_split[2].strip()
        except IndexError:
            continue
        if line_iata == airport_iata:
            return line.split('"')[1]


def prepare_session() -> requests.Session:
    session = requests.Session()
    response = requests.get("https://www.britishairways.com/travel/home/public/en_gb/", headers=HEADERS)
    session.cookies = response.cookies
    session.headers = response.headers
    return session

def prep():
    session = HTMLSession()
    response = requests.get("https://www.britishairways.com/travel/home/public/en_gb/", headers=HEADERS)
    session.cookies = response.cookies
    session.headers = response.headers
    return session


def schedule():
    session = prepare_session()
    destinations = get_destinations()
    for departing_airport in destinations:
        for arrival_airport in destinations:
            departing_airport = "LON"
            arrival_airport = "SYD"
            from_full = get_iata_full_parameter(departing_airport)
            to_full = get_iata_full_parameter(arrival_airport)
            days_count = 0
            date_ = date.today()
            while days_count < 200:
                PARAMS["from-full"] = from_full
                PARAMS["to-full"] = to_full
                PARAMS["from"] = departing_airport
                PARAMS["to"] = arrival_airport
                PARAMS["depDay"] = date_.day
                PARAMS["depMonth"] = date_.strftime("%B")
                PARAMS["retDay"] = date_.day
                PARAMS["retMonth"] = date_.strftime("%B")

                response = session.post(URL, json=PARAMS, headers=HEADERS)
                response.html.render()
                tree = html.fromstring(response.text)
                flights = tree.xpath('//div[@data-tooltip-for="from-header"]/parent::div')
                if not flights:
                    break
                date_ += timedelta(days=days_count)
                days_count += 7
    ...


if __name__ == "__main__":
    schedule()
