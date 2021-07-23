import random

from tensorflow import keras
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from elasticsearch import Elasticsearch, helpers
import json
import random
import pandas as pd
import re
from tensorflow.python.keras.preprocessing.text import Tokenizer, tokenizer_from_json
from tensorflow.python.keras.preprocessing.sequence import pad_sequences
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import string
nltk.download('punkt')
nltk.download('stopwords')


app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates'
            )
cors = CORS(app, resources={r"/*": {"origins": "*"}})

with open('/app/model/tokenizer.json') as f:
    data = json.load(f)
    tokenizer = tokenizer_from_json(data)

model = keras.models.load_model('/app/model/model_trained')
print("API FULL STARTED")

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
    result = {"label": str(predict(data["text"]))}
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

def CleanTokenize(df):
    head_lines = list()
    lines = df["Tweet"].values.tolist()

    for line in lines:
        text = line.lower()
        emoji = re.compile("["
                           u"\U0001F600-\U0001FFFF"  # emoticones
                           u"\U0001F300-\U0001F5FF"  # symboles 
                           u"\U0001F680-\U0001F6FF" 
                           u"\U0001F1E0-\U0001F1FF"  # drapeau (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
        text = text.lower()
        text = emoji.sub(r'', text)
        text = re.sub(r" vs ", "vous", text)
        text = re.sub(r" slt ", "salut", text)
        text = re.sub(r" stp ", "s'il te plaît", text)
        text = re.sub(r" mm ", "meme", text)
        text = re.sub(r" mtn ", "maintenant", text)
        text = re.sub(r" vrm ", "vraiment", text)
        text = re.sub(r" tt ", "tout", text)
        text = re.sub(r" pq ", "pourquoi", text)
        text = re.sub(r" pk ", "pourquoi", text)
        text = re.sub(r" tkt ", "t inquiete", text)
        text = re.sub(r" tqt ", "t inquiete", text)
        text = re.sub(r" t ", "tu es", text)
        text = re.sub(r" tas ", "tu as", text)
        text = re.sub(r" t'as ", "tu as", text)
        text = re.sub(r" t'es ", "tu es", text)
        text = re.sub(r" t'est ", "tu es", text)
        text = re.sub(r" maie ", "mais", text)
        text = re.sub(r" mai ", "mais", text)
        text = re.sub(r" y'a ", "il y a", text)
        text = re.sub(r" ya ", "il y a", text)
        text = re.sub(r" j ", "je", text)
        text = re.sub(r" j ai ", "j'ai", text)
        text = re.sub(r" l ", "l'", text)
        text = re.sub(r" c ", "c'est", text)
        text = re.sub(r" bcp ", "beaucoup", text)
        text = re.sub(r" jvais ", "je vais", text)
        text = re.sub(r" jpense ", "je pense", text)
        text = re.sub(r"[,.\"\'!@#$%^&*(){}?/;`~:<>+=-]", "", text)
        text = re.sub(r"’", "", text)
        text = re.sub(r"»", "", text)
        tokens = word_tokenize(text)
        table = str.maketrans('', '', string.punctuation)
        stripped = [w.translate(table) for w in tokens]
        stop_words = set(stopwords.words("french"))
        words = [w for w in stripped if not w in stop_words]
        head_lines.append(words)
    return head_lines

def predict(s):
    print("le string :")
    print(s)
    recup_data = pd.DataFrame({"Tweet": [s]})
    print("recup_data : ")
    print(recup_data)
    test_lignes = CleanTokenize(recup_data)
    print("test_lignes")
    print(test_lignes)
    test_sequences = tokenizer.texts_to_sequences(test_lignes)
    print("test_sequences")
    print(test_sequences)
    test_review = pad_sequences(test_sequences, maxlen=25, padding='post')
    print("test_review")
    print(test_review)
    prediction = model.predict(test_review)
    prediction *= 100
    print(prediction)
    return prediction[0][0]
