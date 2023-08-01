import os
from flask import Flask, jsonify, request
from flask_mail import Mail, Message
from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv
from src.services import KarmaService
from src.utils import auth
from src.utils import api

# Environment Variables
load_dotenv(find_dotenv())

# Flask
app = Flask(__name__)

# Cors
CORS(app)

# Mail
mail = Mail(app)
app.config['MAIL_SERVER'] = 'smtp.mail.yahoo.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.getenv('FREEFLASH_MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('FREEFLASH_MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@app.route("/")
def default():
    return "Server is online..."


@app.route("/status", methods=['GET'])
def status():
    return jsonify({
        "status": "online"
    })


@app.route("/~", methods=["GET"])
def get_my_ip():
    ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    msg = Message(
        f'IPv4: {ip}',
        sender=os.getenv('FREEFLASH_MAIL_USERNAME'),
        recipients=[os.getenv('FREEFLASH_MAIL_USERNAME')]
    )
    location = api.getIpLocation(ip)
    city = location['city']
    state = location['state']
    zipCode = location['zipCode']
    country = location['country']
    timezone = location['timezone']
    longitude = location['longitude']
    latitude = location['latitude']
    currencyName = location['currencyName']
    currencyCode = location['currencyCode']
    currencySymbol = location['currencySymbol']
    phoneCode = location['phoneCode']

    output = ""
    output += f'City: {city}' + "\n"
    output += f'state: {state}' + "\n"
    output += f'Zip Code: {zipCode}' + "\n"
    output += f'country: {country}' + "\n"
    output += f'Timezone: {timezone}' + "\n"
    output += f'Longitude: {longitude}' + "\n"
    output += f'Latitude: {latitude}' + "\n"
    output += f'Currency: {currencyName} / {currencyCode} / {currencySymbol}' + "\n"
    output += f'Phone Code: {phoneCode}' + "\n"

    msg.body = output
    try:
        mail.send(msg)
    except:
        return ""
    return ""


@app.route("/quote", methods=['GET'])
def quote():
    key = request.headers.get("FREEFLASH_API_KEY")
    if (auth.checkAuth(key)):
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
    if (auth.checkAuth(key)):
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
    if (auth.checkAuth(key)):
        return api.getJoke()
    return "Unauthorized."


@app.route("/insult", methods=['GET'])
def insult():
    key = request.headers.get("FREEFLASH_API_KEY")
    if (auth.checkAuth(key)):
        who = request.args.get("who")
        if (who):
            return api.getInsult(who)
        return "Invalid parameter."
    return "Unauthorized."


@app.route("/google", methods=['POST'])
def google():
    key = request.headers.get("FREEFLASH_API_KEY")
    if (auth.checkAuth(key)):
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
    if (auth.checkAuth(key)):
        text = request.args.get("text")
        if (text):
            return api.getSentimentAnalysis(text)
        return "Invalid parameter."
    return "Unauthorized."


@app.route("/summarize-text", methods=['GET'])
def summarizeText():
    key = request.headers.get("FREEFLASH_API_KEY")
    if (auth.checkAuth(key)):
        text = request.args.get("text")
        if (text):
            return api.getSummarizeText(text)
        return "Invalid parameter."
    return "Unauthorized."


@app.route("/language-detection", methods=['GET'])
def languageDetection():
    key = request.headers.get("FREEFLASH_API_KEY")
    if (auth.checkAuth(key)):
        text = request.args.get("text")
        if (text):
            return api.getLanguageDetection(text)
        return "Invalid parameter."
    return "Unauthorized."


@app.route("/website-extraction", methods=['POST'])
def websiteExtraction():
    key = request.headers.get("FREEFLASH_API_KEY")
    if (auth.checkAuth(key)):
        body = request.json
        text = body["url"]
        if (text):
            return api.getWebsiteExtraction(text)
        return "Invalid parameter."
    return "Unauthorized."


@app.route("/file-extraction", methods=['POST'])
def fileExtraction():
    key = request.headers.get("FREEFLASH_API_KEY")
    if (auth.checkAuth(key)):
        file = request.files['input_file']
        if (file):
            return api.getFileExtraction(file)
        return "Invalid parameter."
    return "Unauthorized."


@app.route("/yoshii", methods=['POST'])
def yoshii():
    key = request.headers.get("FREEFLASH_API_KEY")
    if (auth.checkAuth(key)):
        body = request.json
        input = body["input"]
        if (input):
            return api.getYoshiiChatbot(input)
        return "Invalid parameter."
    return "Unauthorized."


@app.route("/yoshii-karma-add-point", methods=['POST'])
def yoshii_karma_add_point():
    key = request.headers.get("FREEFLASH_API_KEY")
    if (auth.checkAuth(key)):
        body = request.json
        userId = body["userId"]
        serverId = body["serverId"]
        sentiment = body["sentiment"]
        if (userId and serverId and sentiment):
            return KarmaService.addPoint(userId, serverId, sentiment)
        return "Invalid parameter."
    return "Unauthorized."


@app.route("/yoshii-karma-get-point", methods=['POST'])
def yoshii_karma_get_point():
    key = request.headers.get("FREEFLASH_API_KEY")
    if (auth.checkAuth(key)):
        body = request.json
        userId = body["userId"]
        serverId = body["serverId"]
        if (userId and serverId):
            return jsonify({
                "point": KarmaService.getPoint(userId, serverId)
            })
        return "Invalid parameter."
    return "Unauthorized."


@app.route("/yoshii-karma-get-ranking", methods=['POST'])
def yoshii_karma_get_ranking():
    key = request.headers.get("FREEFLASH_API_KEY")
    if (auth.checkAuth(key)):
        body = request.json
        serverId = body["serverId"]
        karmaYear = body["karmaYear"]
        if (serverId):
            return jsonify({
                "ranking": KarmaService.getRanking(serverId, karmaYear)
            })
        return "Invalid parameter."
    return "Unauthorized."


# Main
if __name__ == '__main__':
    app.run()
