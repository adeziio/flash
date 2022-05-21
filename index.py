from flask import Flask, jsonify, request
import api

app = Flask(__name__)


@app.route("/")
def default():
    return "Server is running..."


@app.route("/status", methods=['GET'])
def status():
    return jsonify({
        "status": "online"
    })


@app.route("/quote", methods=['GET'])
def quote():
    auth = request.headers.get("x-api-key")
    if (auth):
        mode = request.args.get("mode")
        if (mode == "today"):
            return api.getTodayQuote()
        elif (mode == "random"):
            return api.getRandomQuote()
        return "Invalid parameter."
    return "Unauthorized."


@app.route("/cat", methods=['GET'])
def cat():
    auth = request.headers.get("x-api-key")
    if (auth):
        mode = request.args.get("mode")
        if (mode == "image"):
            return api.getCatImage()
        elif (mode == "fact"):
            return api.getCatFact()
        return "Invalid parameter."
    return "Unauthorized."


@app.route("/joke", methods=['GET'])
def joke():
    auth = request.headers.get("x-api-key")
    if (auth):
        return api.getJoke()
    return "Unauthorized."


@app.route("/insult", methods=['GET'])
def insult():
    auth = request.headers.get("x-api-key")
    if (auth):
        who = request.args.get("who")
        if (who):
            return api.getInsult(who)
        return "Invalid parameter."
    return "Unauthorized."


@app.route("/google", methods=['POST'])
def google():
    auth = request.headers.get("x-api-key")
    if (auth):
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
    auth = request.headers.get("x-api-key")
    if (auth):
        text = request.args.get("text")
        if (text):
            return api.getSentimentAnalysis(text)
        return "Invalid parameter."
    return "Unauthorized."


@app.route("/yoshii", methods=['GET'])
def yoshii():
    auth = request.headers.get("x-api-key")
    if (auth):
        input = request.args.get("input")
        if (input):
            return api.getYoshiiChatbot(input)
        return "Invalid parameter."
    return "Unauthorized."


if __name__ == '__main__':
    app.run()
