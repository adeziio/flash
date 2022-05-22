from flask import Flask, jsonify, request
from flask_cors import CORS
import api

app = Flask(__name__)
CORS(app)


@app.route("/")
def default():
    return "Server is online..."


@app.route("/status", methods=['GET'])
def status():
    return jsonify({
        "status": "online"
    })


@app.route("/quote", methods=['GET'])
def quote():
    key = request.headers.get("FREEFLASH_API_KEY")
    if (api.checkAuth(key)):
        mode = request.args.get("mode")
        if (mode == "today"):
            return api.getTodayQuote()
        elif (mode == "random"):
            return api.getRandomQuote()
        return "Invalid parameter."
    return "Unauthorized."


@app.route("/cat", methods=['GET'])
def cat():
    key = request.headers.get("FREEFLASH_API_KEY")
    if (api.checkAuth(key)):
        mode = request.args.get("mode")
        if (mode == "image"):
            return api.getCatImage()
        elif (mode == "fact"):
            return api.getCatFact()
        return "Invalid parameter."
    return "Unauthorized."


@app.route("/joke", methods=['GET'])
def joke():
    key = request.headers.get("FREEFLASH_API_KEY")
    if (api.checkAuth(key)):
        return api.getJoke()
    return "Unauthorized."


@app.route("/insult", methods=['GET'])
def insult():
    key = request.headers.get("FREEFLASH_API_KEY")
    if (api.checkAuth(key)):
        who = request.args.get("who")
        if (who):
            return api.getInsult(who)
        return "Invalid parameter."
    return "Unauthorized."


@app.route("/google", methods=['POST'])
def google():
    key = request.headers.get("FREEFLASH_API_KEY")
    if (api.checkAuth(key)):
        body = request.json
        mode = body["mode"]
        search = body["search"]
        if (mode == "image"):
            return api.getGoogleImage(search)
        elif (mode == "search"):
            return api.getGoogleSearch(search)
        return "Invalid parameter."
    return "Unauthorized."


@app.route("/sentiment-analysis", methods=['GET'])
def sentimentAnalysis():
    key = request.headers.get("FREEFLASH_API_KEY")
    if (api.checkAuth(key)):
        text = request.args.get("text")
        if (text):
            return api.getSentimentAnalysis(text)
        return "Invalid parameter."
    return "Unauthorized."


@app.route("/summarize-text", methods=['GET'])
def summarizeText():
    key = request.headers.get("FREEFLASH_API_KEY")
    if (api.checkAuth(key)):
        text = request.args.get("text")
        if (text):
            return api.getSummarizeText(text)
        return "Invalid parameter."
    return "Unauthorized."


@app.route("/language-detection", methods=['GET'])
def languageDetection():
    key = request.headers.get("FREEFLASH_API_KEY")
    if (api.checkAuth(key)):
        text = request.args.get("text")
        if (text):
            return api.getLanguageDetection(text)
        return "Invalid parameter."
    return "Unauthorized."


@app.route("/website-extraction", methods=['POST'])
def websiteExtraction():
    key = request.headers.get("FREEFLASH_API_KEY")
    if (api.checkAuth(key)):
        body = request.json
        text = body["url"]
        if (text):
            return api.getWebsiteExtraction(text)
        return "Invalid parameter."
    return "Unauthorized."


@app.route("/file-extraction", methods=['POST'])
def fileExtraction():
    key = request.headers.get("FREEFLASH_API_KEY")
    if (api.checkAuth(key)):
        file = request.files['input_file']
        if (file):
            return api.getFileExtraction(file)
        return "Invalid parameter."
    return "Unauthorized."


@app.route("/yoshii", methods=['POST'])
def yoshii():
    key = request.headers.get("FREEFLASH_API_KEY")
    if (api.checkAuth(key)):
        body = request.json
        input = body["input"]
        if (input):
            return api.getYoshiiChatbot(input)
        return "Invalid parameter."
    return "Unauthorized."


if __name__ == '__main__':
    app.run()
