from flask import Flask, Response
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time, os

app = Flask(__name__)

@app.route("/")
def index():
    return "API OK. Va sur /cookie"

@app.route("/cookie")
def get_cookie():
    options = Options()
    options.binary_location = "/usr/bin/chromium"

    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument("--single-process")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--user-data-dir=/tmp/chrome-user-data")

    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://5afterdark.mom/")
        time.sleep(1)

        driver.get("https://5afterdark.mom/video/7e4de128-b10f-dc2b-0542-7590c441630e")
        time.sleep(2)

        for cookie in driver.get_cookies():
            if cookie["name"] == "__illit":
                return Response(cookie["value"], mimetype="text/plain")

        return Response("Cookie __illit non trouvé", status=404, mimetype="text/plain")

    except Exception as e:
        return Response(f"Erreur : {e}", status=500, mimetype="text/plain")

    finally:
        driver.quit()
