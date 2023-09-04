from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth

from time import sleep
from random import random


def pause_for(seconds: int, fudge: int = 1):
    sleep(seconds+random() * fudge)


def driver(headless=True):

    # Set Browser Options
    opts = Options()
    if headless:
        opts.add_argument('--headless=new')
    opts.add_argument('start-maximized')
    opts.add_argument('disable-infobars')
    opts.add_argument('--disable-notifications')
    opts.add_argument('--disable-gpu')
    opts.add_argument('--mute-audio')
    opts.add_argument('log-level=3')

    # Desired Capabilities
    loggingPrefs = {}
    loggingPrefs['performance'] = "ALL"
    opts.set_capability('goog:loggingPrefs', loggingPrefs)

    # Launch Browser
    driver = webdriver.Chrome(options=opts)

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
