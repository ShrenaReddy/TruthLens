import pandas as pd
import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

# Load dataset (should now contain clean_title)
data = pd.read_csv("data/cleaned_news.csv")

# Remove empty values
data = data.dropna(subset=["clean_title"])
data = data[data["clean_title"].str.strip() != ""]

X = data["clean_title"]
y = data["label"]

# TF-IDF (optimized for short text like titles)
vectorizer = TfidfVectorizer(
    max_features=5000,      # slightly reduced for titles
    ngram_range=(1,2),
    min_df=2
)

X_tfidf = vectorizer.fit_transform(X)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X_tfidf, y, test_size=0.2, random_state=42
)

# Save
os.makedirs("models", exist_ok=True)

pickle.dump(vectorizer, open("models/vectorizer.pkl", "wb"))
pickle.dump(X_train, open("models/X_train.pkl", "wb"))
pickle.dump(X_test, open("models/X_test.pkl", "wb"))
pickle.dump(y_train, open("models/y_train.pkl", "wb"))
pickle.dump(y_test, open("models/y_test.pkl", "wb"))

print("✅ Day 3 (title-based) completed")