from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/")
def default():
    return "Server is running..."


@app.route("/status", methods=['GET'])
def getStatus():
    return jsonify({
        "status": "looks good!"
    })


if __name__ == '__main__':
    app.run()
