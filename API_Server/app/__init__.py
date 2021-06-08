import random

from flask import Flask, request, jsonify
import random
def create_app():
    app = Flask(__name__)

    @app.route('/')
    def homepage():
        return 'This is the homepage'

    @app.route('/evaluate_sarcasm', methods=['POST'])
    def evaluate_sarcasm():
        data = request.json
        print(data["text"])
        result = {"score": predict(data["text"])}
        return jsonify(result)

    def predict(text):
        score = random.random() * 100
        return score

    return app