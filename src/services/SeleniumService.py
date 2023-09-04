import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth

from time import sleep
from random import random


def pause_for(seconds: int, fudge: int = 1):
    sleep(seconds+random() * fudge)


def driver(headless=True):

    # Set Browser Options
    options = webdriver.ChromeOptions()
    service = webdriver.ChromeService(
        executable_path="./src/services/chromedriver.exe")
    if headless:
        options.add_argument('--headless=new')
    options.add_argument('--start-maximized')
    options.add_argument('disable-infobars')
    options.add_argument('--disable-notifications')
    options.add_argument('--disable-gpu')
    options.add_argument('--mute-audio')
    options.add_argument('log-level=3')

    # Desired Capabilities
    loggingPrefs = {}
    loggingPrefs['performance'] = "ALL"
    options.set_capability('goog:loggingPrefs', loggingPrefs)

    # Launch Browser
    driver = webdriver.Chrome(service=service, options=options)

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    driver.delete_all_cookies()
    return driver
