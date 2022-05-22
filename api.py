import os
import re
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
    payload = json.dumps({
        "language": "english",
        "text": text
    })
    headers = {
        'content-type': "application/json",
        'x-rapidapi-host': "text-analysis12.p.rapidapi.com",
        'x-rapidapi-key': os.getenv("RAPID_API_KEY")
    }

    return requests.post(url, data=payload, headers=headers).json()


def getSummarizeText(text):
    url = "https://text-analysis12.p.rapidapi.com/summarize-text/api/v1.1"
    payload = json.dumps({
        "language": "english",
        "text": text
    })
    headers = {
        'content-type': "application/json",
        'x-rapidapi-host': "text-analysis12.p.rapidapi.com",
        'x-rapidapi-key': os.getenv("RAPID_API_KEY")
    }

    return requests.post(url, data=payload, headers=headers).json()


def getLanguageDetection(text):
    url = "https://text-analysis12.p.rapidapi.com/language-detection/api/v1.1"
    payload = json.dumps({
        "text": text
    })
    headers = {
        'content-type': "application/json",
        'x-rapidapi-host': "text-analysis12.p.rapidapi.com",
        'x-rapidapi-key': os.getenv("RAPID_API_KEY")
    }

    return requests.post(url, data=payload, headers=headers).json()


def getWebsiteExtraction(text):
    url = "https://text-analysis12.p.rapidapi.com/website-extraction/api/v1.3"
    payload = "language=english&url=" + text
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'x-rapidapi-host': "text-analysis12.p.rapidapi.com",
        'x-rapidapi-key': os.getenv("RAPID_API_KEY")
    }

    return requests.post(url, data=payload, headers=headers).json()


def getFileExtraction(file):
    # todo: need to fix this api
    url = "https://text-analysis12.p.rapidapi.com/text-mining/api/v1.1"

    payload = {
        "input_file": file
    }

    headers = {
        "content-type": "multipart/form-data; boundary=---011000010111000001101001",
        "x-rapidapi-host": "text-analysis12.p.rapidapi.com",
        'x-rapidapi-key': os.getenv("RAPID_API_KEY")
    }
    res = requests.post(url, data=payload, headers=headers)
    return res.json()


def getYoshiiChatbot(input):
    input = input.lower().replace("yoshii", "RoboMatic")
    input = input.lower().replace("+", "%2B")
    input = input.lower().replace("'", "")

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
    ouput = res['out']
    ouput = ouput.replace("I said it before, ", "")
    ouput = ouput.replace("RoboMatic", "yoshii")
    ouput = ouput.replace("Ehab Elagizy", "Aden Tran")
    ouput = ouput.replace("back in 2001", "back in 2021")
    ouput = ouput.replace("since 1995", "since 2021")
    ouput = ouput.replace("Later in 2011", "In 2021")
    ouput = ouput.replace("Egyptian", "Vietnamese")

    return {
        "ouput": ouput
    }
