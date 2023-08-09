import os
import requests
import json
import urllib.parse


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


def getIpLocation(ip):
    querystring = {"ip": ip, "apikey": os.getenv('FIND_ANY_IP_KEY')}
    headers = {
        'x-rapidapi-host': "find-any-ip-address-or-domain-location-world-wide.p.rapidapi.com",
        'x-rapidapi-key': os.getenv('RAPID_API_KEY')
    }

    return requests.get("https://find-any-ip-address-or-domain-location-world-wide.p.rapidapi.com/iplocation", headers=headers, params=querystring).json()


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
    url = "https://text-sentiment.p.rapidapi.com/analyze"
    payload = f"text={text.encode('utf-8')}"
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Host": "text-sentiment.p.rapidapi.com",
        'x-rapidapi-key': os.getenv("RAPID_API_KEY")
    }

    response = requests.post(url, data=payload, headers=headers).json()
    pos = int(response['pos'])
    neg = int(response['neg'])
    sentiment = "neutral"
    if (pos > neg):
        sentiment = "positive"
    elif (pos < neg):
        sentiment = "negative"
    return {'sentiment': sentiment}


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
    input = input.lower()
    model = "language"
    if "image" in input:
        model = "image"
    payload = json.dumps({
        "model": model,
        "input": input
    })
    headers = {
        "Content-Type": "application/json",
        "GIDEON_API_KEY":  os.getenv("GIDEON_API_KEY")
    }
    res = requests.post(
        "https://gideon-ai.vercel.app/openai", data=payload, headers=headers).json()
    output = res['output']
    return {
        "output": output
    }
