from flask import Flask, request, jsonify
import pickle
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

model = pickle.load(open("../models/best_model.pkl", "rb"))
vectorizer = pickle.load(open("../models/vectorizer.pkl", "rb"))

stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

def preprocess(title):
    title = title.lower()
    title = re.sub(r"[^a-zA-Z\s]", "", title)

    words = title.split()
    words = [stemmer.stem(w) for w in words if w not in stop_words and len(w) > 2]

    return " ".join(words)

@app.route("/predict", methods=["POST"])
@app.route("/")
def home():
    return "Fake News Detector API Running 🚀"
def predict():
    title = request.json["title"]

    cleaned = preprocess(title)
    vectorized = vectorizer.transform([cleaned])
    prediction = model.predict(vectorized)[0]

    return jsonify({
        "result": "REAL ✅" if prediction == 1 else "FAKE ❌"
    })

app.run(debug=True)