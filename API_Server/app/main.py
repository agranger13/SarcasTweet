import random

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import random

app = Flask(__name__)
cors = CORS(app, resources={r"/evaluate_sarcasm": {"origins": "*"}})

@app.route('/')
def homepage():
    return 'This is the homepage'

@app.route('/evaluate_sarcasm', methods=['POST'])
@cross_origin()
def evaluate_sarcasm():
    print("start evaluation")
    print(request)
    data = request.json
    print(data["text"])
    result = {"score": predict(data["text"])}
    return jsonify(result)

def predict(text):
    score = random.random() * 100
    return score
