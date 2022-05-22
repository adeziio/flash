import os
import requests
import json


def checkAuth(key):
    if (key == os.getenv('FREEFLASH_API_KEY')):
        return True
    return False


def getRandomQuote():
    return requests.get("https://zenquotes.io/api/random").json()[0]


def getTodayQuote():
    return requests.get("https://zenquotes.io/api/today").json()[0]


def getCatImage():
    return requests.get("https://api.thecatapi.com/v1/images/search").json()[0]


def getCatFact():
    return requests.get("https://catfact.ninja/fact").json()


def getJoke():
    return requests.get("https://v2.jokeapi.dev/joke/Any?type=single").json()


def getInsult(who):
    return requests.get("https://insult.mattbas.org/api/en/insult.txt?who="+who.capitalize()).text


def getGoogleImage(search):
    headers = {
        'x-rapidapi-host': "google-search3.p.rapidapi.com",
        'x-rapidapi-key': os.getenv('RAPID_API_KEY')
    }
    return requests.get("https://google-search3.p.rapidapi.com/api/v1/image/q=" +
                        search, headers=headers).json()


def getGoogleSearch(search):
    headers = {
        'x-rapidapi-host': "google-search3.p.rapidapi.com",
        'x-rapidapi-key': os.getenv('RAPID_API_KEY')
    }
    return requests.get("https://google-search3.p.rapidapi.com/api/v1/search/q=" +
                        search, headers=headers).json()


def getSentimentAnalysis(text):
    url = "https://text-analysis12.p.rapidapi.com/sentiment-analysis/api/v1.1"
    payload = {
        "language": "english",
        "text": text
    }
    headers = {
        'content-type': "application/json",
        'x-rapidapi-host': "text-analysis12.p.rapidapi.com",
        'x-rapidapi-key': os.getenv("RAPID_API_KEY")
    }

    return requests.post(url, data=json.dumps(
        payload), headers=headers).json()


def getSummarizeText(text):
    url = "https://text-analysis12.p.rapidapi.com/summarize-text/api/v1.1"
    payload = {
        "language": "english",
        "text": text
    }
    headers = {
        'content-type': "application/json",
        'x-rapidapi-host': "text-analysis12.p.rapidapi.com",
        'x-rapidapi-key': os.getenv("RAPID_API_KEY")
    }

    return requests.post(url, data=json.dumps(
        payload), headers=headers).json()


def getLanguageDetection(text):
    url = "https://text-analysis12.p.rapidapi.com/language-detection/api/v1.1"
    payload = {
        "text": text
    }
    headers = {
        'content-type': "application/json",
        'x-rapidapi-host': "text-analysis12.p.rapidapi.com",
        'x-rapidapi-key': os.getenv("RAPID_API_KEY")
    }

    return requests.post(url, data=json.dumps(
        payload), headers=headers).json()


def getYoshiiChatbot(input):
    input = input.lower().replace("yoshii", "RoboMatic")
    input = input.lower().replace("+", "plus")
    url = "https://robomatic-ai.p.rapidapi.com/api.php"

    payload = "in=" + input + \
        "F&op=in&cbot=1&SessionID=RapidAPI1&ChatSource=RapidAPI&cbid=1&key=" + \
        os.getenv("ROBOMATIC_KEY")
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'x-rapidapi-host': "robomatic-ai.p.rapidapi.com",
        'x-rapidapi-key': os.getenv("RAPID_API_KEY")
    }

    res = requests.request(
        "POST", url, data=payload, headers=headers).json()
    out = res['out']
    out = out.replace("I said it before, ", "")
    out = out.replace("RoboMatic", "yoshii")
    out = out.replace("Ehab Elagizy", "Aden Tran")
    out = out.replace("back in 2001", "back in 2021")
    out = out.replace("since 1995", "since 2021")
    out = out.replace("Later in 2011", "In 2021")
    out = out.replace("Egyptian", "Vietnamese")
    return {
        "out": out
    }
