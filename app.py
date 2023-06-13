from fb_hashtag_scraper import scrapper, test
from flask import Flask, request, render_template,Response,stream_with_context
from confluent_kafka import Producer
from nltk.corpus import stopwords
import nltk
from nltk.stem import WordNetLemmatizer
import re
from consumer import consumer
from producer import producer
import json 
from producer_consumer import producer_consumer
from detoxify import Detoxify
from pymongo import MongoClient

lemma = WordNetLemmatizer()
swords = stopwords.words("english")

host = 'localhost'
port = 27017


app = Flask(__name__)

def clean_data(txt):
    txt = re.sub(r'#', '', txt)
    txt = re.sub(r'https?:\/\/[A-Za-z0-9\.\/]+', '', txt)
    text = nltk.word_tokenize(txt.lower())
    text = [lemma.lemmatize(word) for word in text]
    text = [word for word in text if word not in swords]
    text = " ".join(text)
    return text


@app.route('/', methods=['GET'])
def home():
    cleaned_data = []
    json_data = []
    id = 0
    for data_item in scrapper():
        cleaned_item = clean_data(data_item)
        item = {"id": id, "content": cleaned_item}
        cleaned_data.append(cleaned_item)
        json_data.append(item)
        id+=1
    with open('data.json', "w") as file:
        json.dump(json_data, file)
    return render_template('cleaned_data.html', data=cleaned_data)

# send data using kafka to flask app
@app.route('/consumedata', methods=["GET"])
def consume():
    def generate_data():
        producer()
        for data in consumer():
            print(data)
            yield data

    def generate_html():
        yield '<html>'
        yield '<body>'
        yield '<h1>Data:</h1>'
        for data in generate_data():
            yield f'<p>{data}</p>'
        yield '</body>'
        yield '</html>'

    return app.response_class(stream_with_context(generate_html()))

#use detoxify model and load data to mongodb
@app.route('/detoxify', methods=['GET'])
def detoxify():
    data = []
    client = MongoClient(host, port)
    db = client['mydatabase']
    collection = db['mycollection']

    with open('data.json', 'r') as file:
        data = json.load(file)
    
    updated_data = []  # Create a new list to store updated items
    
    for item in data:
        results = Detoxify('multilingual').predict([item.get('content')])
        item.update(results)
        updated_data.append(item)  # Append the updated item to the new list
        result = collection.insert_one(updated_data)
    return render_template('detox.html', data=updated_data)


if __name__ == '__main__':
    app.debug = True
    app.run()