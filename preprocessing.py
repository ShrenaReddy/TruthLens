import pickle
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Load model
model = pickle.load(open("models/best_model.pkl", "rb"))
vectorizer = pickle.load(open("models/vectorizer.pkl", "rb"))

stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

def preprocess_title(title):
    title = title.lower()
    title = re.sub(r"http\S+|www\S+", "", title)
    title = re.sub(r"[^a-zA-Z\s]", "", title)

    words = title.split()

    cleaned_words = []
    for word in words:
        if word not in stop_words and len(word) > 2:
            cleaned_words.append(stemmer.stem(word))

    return " ".join(cleaned_words)

def predict_news(title):
    cleaned = preprocess_title(title)

    print("Cleaned:", cleaned)

    if len(cleaned.split()) < 3:   # titles are shorter than full text
        return "⚠️ Please enter a longer title"

    vectorized = vectorizer.transform([cleaned])
    prediction = model.predict(vectorized)[0]

    if prediction == 1:
        return "REAL NEWS ✅"
    else:
        return "FAKE NEWS ❌"

# Run
if __name__ == "__main__":
    user_input = input("Enter news title:\n>> ")
    print("\nPrediction:", predict_news(user_input))