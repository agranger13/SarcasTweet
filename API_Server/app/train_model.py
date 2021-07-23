import numpy as np
import pandas as pd
import os
import re  # Regular expression
import elasticsearch
import elasticsearch.helpers
import string
import nltk
import io
import json

nltk.download('punkt')
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from tensorflow import keras
from tensorflow.python.keras.preprocessing.text import Tokenizer
from tensorflow.python.keras.preprocessing.sequence import pad_sequences
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, LSTM, Bidirectional
from tensorflow.python.keras.layers.embeddings import Embedding

host = 'search-sarcastweet-7w4lvds7cvubzgyd4i4kq72gwe.us-east-2.es.amazonaws'

es = elasticsearch.Elasticsearch(
    hosts=["https://root_user:M9p7r3u*@search-sarcastweet-7w4lvds7cvubzgyd4i4kq72gwe.us-east-2.es.amazonaws.com"],
)

es.info()
body = {"query": {"match_all": {}}}
results = elasticsearch.helpers.scan(es, query=body, index="tweets", request_timeout=30)
data = pd.DataFrame.from_dict([document['_source'] for document in results])

# Remove unused columns and clean Na
data.dropna(subset=["Tweet", "label"], inplace=True)

# endpoint = 'https://search-projet-final-7oxdpiy44ynvktr43nimfxpjuy.us-east-2.es.amazonaws.com'
# results = requests.get(endpoint + '/tweets/_search', auth=('root_user','M9p7r3u*')).json()
# print(results['hits']["hits"])
# data = pd.DataFrame.from_dict([document["_source"] for document in results['hits']["hits"]])
data.loc[data['label'] == "Oui", 'sarcastic'] = 1
data.loc[data['label'] == "Non", 'sarcastic'] = 0
data['sarcastic'] = data["sarcastic"].astype(int)
data = data.drop(columns="label")
data.head()


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


head_lines = CleanTokenize(data)

validation_split = 0.2
max_length = 32
tokenizer_obj = Tokenizer()
tokenizer_obj.fit_on_texts(head_lines)
sequences = tokenizer_obj.texts_to_sequences(head_lines)

word_index = tokenizer_obj.word_index
print("unique tokens - ", len(word_index))
vocab_size = len(tokenizer_obj.word_index) + 1
print('vocab size -', vocab_size)

lines_pad = pad_sequences(sequences, maxlen=max_length, padding='post')
sentiment = data['sarcastic'].values

indices = np.arange(lines_pad.shape[0])
np.random.shuffle(indices)
lines_pad = lines_pad[indices]
sentiment = sentiment[indices]
num_validation_samples = int(validation_split * lines_pad.shape[0])

X_train_pad = lines_pad[:-num_validation_samples]
y_train = sentiment[:-num_validation_samples]
X_test_pad = lines_pad[-num_validation_samples:]
y_test = sentiment[-num_validation_samples:]

vector_rep = {}
dimention = 100
f = open(os.path.join('glove.twitter.27B.100d.txt'), encoding="utf-8")
for line in f:
    values = line.split()
    word = values[0]
    coefs = np.asarray(values[1:], dtype='float32')
    vector_rep[word] = coefs
f.close()

matrix = np.zeros((len(word_index) + 1, dimention))
c = 0
for word, i in word_index.items():
    vector = vector_rep.get(word)
    if vector is not None:
        c += 1
        matrix[i] = vector

layer = Embedding(len(word_index) + 1,
                  dimention,
                  weights=[matrix],
                  input_length=max_length,
                  trainable=False)

model = Sequential()
model.add(layer)
model.add(Bidirectional(LSTM(units=128, recurrent_dropout=0.15, dropout=0.25)))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['acc'])
model.fit(X_train_pad, y_train, batch_size=32, epochs=30, validation_data=(X_test_pad, y_test), verbose=2)


def is_ironique(s, model_iro):
    recup_data = pd.DataFrame({"Tweet":[s]})
    test_lignes = CleanTokenize(recup_data)
    test_sequences = tokenizer_obj.texts_to_sequences(test_lignes)
    test_review = pad_sequences(test_sequences, maxlen=max_length, padding='post')
    prediction = model_iro.predict(test_review)
    prediction*=100
    return prediction[0][0]

keras.models.save_model(model, "./model/model_trained")

tokenizer_json = tokenizer_obj.to_json()
with io.open('tokenizer.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(tokenizer_json, ensure_ascii=False))

print(is_ironique("go faire ma 2eme dose, a moi la 5G",model))
print(is_ironique("J'aime bien ce film.",model))
print(is_ironique("Genial, encore un mec bizarre",model))
print(is_ironique("How it started:       How it's going:",model))

model2 = keras.models.load_model('./model/model_trained')
print("\nmodel2 :")
print(is_ironique("go faire ma 2eme dose, a moi la 5G",model2))
print(is_ironique("J'aime bien ce film.",model2))
print(is_ironique("Genial, encore un mec bizarre",model2))
print(is_ironique("How it started:       How it's going:",model2))
print(is_ironique("Uranus Et Pluton🎶 🎺Airelle Besson More Greek influences in the naming of many celestial bodies, including Alpha Centauri!",model2))
print(is_ironique("Athènes en Grèce 🇬🇷, où les Jeux Olympiques ont été re-fondés en 1896. Les Jeux antiques se tenaient eux à Olympie il y a près de 30 siècles !",model2))

