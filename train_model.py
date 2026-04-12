import pandas as pd
import pickle
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# -------------------------------
# Preprocessing
# -------------------------------
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)

    words = text.split()
    words = [stemmer.stem(w) for w in words if w not in stop_words and len(w) > 2]

    return " ".join(words)

# -------------------------------
# Load dataset
# -------------------------------
data = pd.read_csv("data/news_dataset.csv")

# Clean text again properly
data["clean_text"] = data["text"].apply(preprocess_text)

# Remove empty rows
data = data[data["clean_text"].str.strip() != ""]

X = data["clean_text"]
y = data["label"]

# -------------------------------
# TF-IDF (STRONG VERSION)
# -------------------------------
vectorizer = TfidfVectorizer(
    max_features=10000,
    ngram_range=(1,2),
    min_df=3,
    max_df=0.9
)

X_tfidf = vectorizer.fit_transform(X)

# -------------------------------
# Train/Test Split
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X_tfidf, y, test_size=0.2, random_state=42
)

# -------------------------------
# Model
# -------------------------------
model = LogisticRegression(max_iter=3000)

print("Training model...")
model.fit(X_train, y_train)

print("Accuracy:", model.score(X_test, y_test))

# -------------------------------
# Save
# -------------------------------
pickle.dump(model, open("models/best_model.pkl", "wb"))
pickle.dump(vectorizer, open("models/vectorizer.pkl", "wb"))

print("✅ Model trained & saved successfully")