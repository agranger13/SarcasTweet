import random
from tensorflow import keras
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from elasticsearch import Elasticsearch, helpers
import json
import random

from API_Server.app.train_model import train_model

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
    result = {"label": predict(data["text"])}
    return jsonify(result)


@app.route('/send_feedback', methods=['POST'])
@cross_origin()
def send_feedback():
    print("sending feedback")
    es = ES_Data()
    data = request.json
    print(data["text"]," => ",data["label"])
    return es.send(data["text"],data["label"])

class ES_Data:
    def __init__(self):
        self.es = Elasticsearch(
            [
                'https://root_user:M9p7r3u*@search-sarcastweet-7w4lvds7cvubzgyd4i4kq72gwe.us-east-2.es.amazonaws.com/'
            ],
            timeout=100
        )

    def send(self, text, label):
        if label:
            tlabel="Oui"
        else:
            tlabel="Non"

        body = {"text": text, "label": tlabel}
        print(json.dumps(body))

        return self.es.index(index="tweets", body=body)

def predict(s):
    train_model.is_ironique()