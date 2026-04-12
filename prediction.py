# =====================================
# Fake News Detection - Day 5
# Prediction System (Title-Based)
# =====================================

import pickle
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# -------------------------------
# Step 1: Load model & vectorizer
# -------------------------------
try:
    model = pickle.load(open("models/best_model.pkl", "rb"))
    vectorizer = pickle.load(open("models/vectorizer.pkl", "rb"))
    print("Model and vectorizer loaded!")
except:
    print("Error loading model/vectorizer. Run Day 4 first.")
    exit()

# -------------------------------
# Step 2: Setup preprocessing tools
# -------------------------------
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

# -------------------------------
# Step 3: Preprocessing function
# -------------------------------
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

# -------------------------------
# Step 4: Prediction function
# -------------------------------
def predict_news(title):
    
    cleaned = preprocess_title(title)
    
    print("Original Title:", title)
    print("Cleaned Title:", cleaned)
    
    # Handle very short input (titles are small)
    if len(cleaned.split()) < 3:
        return "⚠️ Please enter a longer title"
    
    vectorized = vectorizer.transform([cleaned])
    
    prediction = model.predict(vectorized)[0]
    
    print("Raw prediction:", prediction)
    
    if prediction == 0:
        return "FAKE NEWS ❌"
    else:
        return "REAL NEWS ✅"

# -------------------------------
# Step 5: Test with user input
# -------------------------------
if __name__ == "__main__":
    
    print("\nEnter a news title:")
    user_input = input(">> ")
    
    result = predict_news(user_input)
    
    print("\nPrediction:", result)