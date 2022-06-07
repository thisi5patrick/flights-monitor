from flask import Flask
import requests
import urllib.parse

app = Flask(__name__)


@app.route("/")
def hello_world():  # put application's code here
    from constants.constants import OPEN_SKY_ENDPOINT

    url = urllib.parse.urljoin(OPEN_SKY_ENDPOINT, "flights/arrival")
    print(url)
    response = requests.get(
        url, params={"airport": "EPWA", "begin": 1654385232, "end": 1654585254}
    )
    return response.text


if __name__ == "__main__":
    app.run()
