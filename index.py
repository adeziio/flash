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
        result = api.getTodayQuote()[0]
        return jsonify({
            'q': result['q'],
            'a': result['a'],
            'h': result['h']
        })
    elif (mode == "random"):
        result = api.getRandomQuote()[0]
        return jsonify({
            'q': result['q'],
            'a': result['a'],
            'h': result['h']
        })


if __name__ == '__main__':
    app.run()
