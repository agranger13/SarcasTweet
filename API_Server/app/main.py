import random

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from elasticsearch import Elasticsearch, helpers
import json
import random

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

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


@app.route('/send_feedback', methods=['POST'])
@cross_origin()
def send_feedback():
    print("sending feedback")
    es = ES_Data()
    data = request.json
    print(data["text"]," => ",data["label"])
    es.send(data["text"],data["label"])

def predict(text):
    score = random.random() * 100
    return score

class ES_Data:
    def __init__(self):
        self.es = Elasticsearch(
            [
                'https://fpi04y6zo7:k6ezgcj8zp@elm-236927195.eu-west-1.bonsaisearch.net:443'
            ],
            timeout=100
        )

    def send(self, text, label):
        body = {"text": text, "label": label}
        print(json.dumps(body))

        print(self.es.index(index="feedback", body=body))

def predict(text):
    score = random.random() * 100
    return score
