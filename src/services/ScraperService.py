import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from src.services import SeleniumService


def scrape_bitchute(driver: webdriver, url):
    data = []
    try:
        driver.get(url)
        WebDriverWait(driver, 30).until(EC.visibility_of_element_located(
            (By.XPATH, "//ul[@id='comment-list']")))
        content = driver.page_source
        soup = BeautifulSoup(content, 'html.parser')

        comments = soup.find_all(attrs={'class': 'content'})
        for comment in comments:
            data.append(comment.text)
    except:
        pass
    return data


def getDomain(url):
    if "www.bitchute.com" in url:
        return "bitchute"


def getComments(url):
    comments = []
    scraper = getDomain(url)

    driver = SeleniumService.driver()
    if scraper == "bitchute":
        comments = scrape_bitchute(driver, url)

    return comments
