from flask import Flask, Response
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time, os, tempfile, traceback

app = Flask(__name__)

@app.route("/")
def index():
    return "API OK. Va sur /cookie"

@app.route("/cookie")
def get_cookie():
    log_path = "/tmp/chromedriver.log"

    try:
        options = Options()
        options.binary_location = "/usr/bin/chromium"

        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-setuid-sandbox")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--window-size=1920,1080")
        options.add_argument(f"--user-data-dir={tempfile.mkdtemp()}")

        service = Service(
            "/usr/bin/chromedriver",
            service_args=["--verbose"],
            log_output=log_path
        )

        driver = webdriver.Chrome(service=service, options=options)

        try:
            driver.get("https://5afterdark.mom/")
            time.sleep(2)

            driver.get("https://5afterdark.mom/video/7e4de128-b10f-dc2b-0542-7590c441630e")
            time.sleep(3)

            for cookie in driver.get_cookies():
                if cookie["name"] == "__illit":
                    return Response(cookie["value"], mimetype="text/plain")

            return Response("Cookie __illit non trouvé", status=404)

        finally:
            driver.quit()

    except Exception as e:
        chrome_log = ""
        if os.path.exists(log_path):
            with open(log_path, "r", errors="ignore") as f:
                chrome_log = f.read()[-4000:]

        return Response(
            "ERREUR:\n"
            + str(e)
            + "\n\nTRACEBACK:\n"
            + traceback.format_exc()
            + "\n\nCHROMEDRIVER LOG:\n"
            + chrome_log,
            status=500,
            mimetype="text/plain"
        )
