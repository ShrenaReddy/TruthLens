# combine.py
import os
import pandas as pd

# -------------------- LOAD DATA --------------------
try:
    fake = pd.read_csv("fake_news_articles.csv")
    real = pd.read_csv("news_articles.csv")
except FileNotFoundError as e:
    print(f"❌ File not found: {e}")
    exit()

# -------------------- STANDARDIZE COLUMNS --------------------
# Add missing 'content' column if not present
if 'content' not in fake.columns:
    fake['content'] = ""
if 'content' not in real.columns:
    real['content'] = ""

# Keep only required columns
columns = ['headline', 'url', 'content', 'source', 'label']
fake = fake[columns]
real = real[columns]

# -------------------- COMBINE & SHUFFLE --------------------
dataset = pd.concat([fake, real], ignore_index=True)
dataset = dataset.sample(frac=1, random_state=42).reset_index(drop=True)

# -------------------- CREATE FOLDER IF NOT EXISTS --------------------
output_folder = "data"
os.makedirs(output_folder, exist_ok=True)

# -------------------- SAVE TO CSV --------------------
output_file = os.path.join(output_folder, "combine_news_dataset.csv")
dataset.to_csv(output_file, index=False, encoding='utf-8-sig')  # safer for Excel on Windows
try:
    print(f"[SUCCESS] Combined dataset saved as {output_file}")
except UnicodeEncodeError:
    print("[SUCCESS] Combined dataset saved (console may not support emojis).")

print(f"Total rows: {dataset.shape[0]}")