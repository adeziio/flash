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
    mode = request.args.get("mode")
    if (mode == "today"):
        return api.getTodayQuote()
    elif (mode == "random"):
        return api.getRandomQuote()
    return "Invalid parameter."


@app.route("/cat", methods=['GET'])
def cat():
    mode = request.args.get("mode")
    if (mode == "image"):
        return api.getCatImage()
    elif (mode == "fact"):
        return api.getCatFact()
    return "Invalid parameter."


@app.route("/joke", methods=['GET'])
def joke():
    return api.getJoke()


@app.route("/google", methods=['POST'])
def google():
    body = request.json
    mode = body["mode"]
    search = body["search"]
    if (mode == "image"):
        return api.getGoogleImage(search)
    elif (mode == "search"):
        return api.getGoogleSearch(search)
    return "Invalid parameter."


@app.route("/sentiment-analysis", methods=['GET'])
def sentimentAnalysis():
    text = request.args.get("text")
    if (text):
        return api.getSentimentAnalysis(text)
    return "Invalid parameter."


@app.route("/yoshii", methods=['GET'])
def yoshii():
    input = request.args.get("input")
    if (input):
        return api.getYoshiiChatbot(input)
    return "Invalid parameter."


if __name__ == '__main__':
    app.run()
