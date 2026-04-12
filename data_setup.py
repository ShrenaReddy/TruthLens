import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Load dataset (from Day 1)
data = pd.read_csv("data/news_dataset.csv")

stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

def clean_title(title):
    title = str(title).lower()
    title = re.sub(r"http\S+|www\S+", "", title)
    title = re.sub(r"[^a-zA-Z\s]", "", title)

    words = title.split()

    cleaned_words = []
    for word in words:
        if word not in stop_words and len(word) > 2:
            cleaned_words.append(stemmer.stem(word))

    return " ".join(cleaned_words)

# Apply cleaning
data["clean_title"] = data["title"].apply(clean_title)


# Save cleaned dataset
data.to_csv("data/cleaned_news.csv", index=False)

print("✅ Cleaned data saved as cleaned_news.csv")
print(data.head())