import pickle
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

model = pickle.load(open("models/best_model.pkl", "rb"))
vectorizer = pickle.load(open("models/vectorizer.pkl", "rb"))

stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", "", text)

    words = text.split()
    words = [stemmer.stem(w) for w in words if w not in stop_words and len(w) > 2]

    return " ".join(words)

def predict_news(text):
    cleaned = preprocess_text(text)

    if len(cleaned.split()) < 5:
        return "⚠️ Enter proper news article"

    vec = vectorizer.transform([cleaned])
    pred = model.predict(vec)[0]

    return "REAL NEWS ✅" if pred == 1 else "FAKE NEWS ❌"

if __name__ == "__main__":
    text = input("Enter news:\n>> ")
    print(predict_news(text))