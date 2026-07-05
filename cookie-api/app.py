from flask import Flask, Response
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os

app = Flask(__name__)

@app.route("/")
def index():
    return "API OK. Va sur /cookie"

@app.route("/cookie")
def get_cookie():
    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/chromium"

    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get("https://5afterdark.mom/")
        time.sleep(1)

        driver.get("https://5afterdark.mom/video/7e4de128-b10f-dc2b-0542-7590c441630e")
        time.sleep(2)

        cookies = driver.get_cookies()

        for cookie in cookies:
            if cookie["name"] == "__illit":
                return Response(cookie["value"], mimetype="text/plain")

        return Response("Cookie __illit non trouvé", status=404, mimetype="text/plain")

    except Exception as e:
        return Response(f"Erreur : {str(e)}", status=500, mimetype="text/plain")

    finally:
        driver.quit()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)