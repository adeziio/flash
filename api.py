import requests


def getRandomQuote():
    return requests.get("https://zenquotes.io/api/random").json()


def getTodayQuote():
    return requests.get("https://zenquotes.io/api/today").json()
