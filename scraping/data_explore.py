# data_explore.py
import pandas as pd
import os

# -------------------- LOAD COMBINED DATASET --------------------
combined_file = "data/combined_news_dataset.csv"  # Original combined dataset
clean_file = "data/news_dataset.csv"             # Cleaned dataset to save

if not os.path.exists(combined_file):
    print(f"[ERROR] File not found: {combined_file}")  # ✅ Windows-safe
    exit()

dataset = pd.read_csv(combined_file, encoding='utf-8-sig')

# -------------------- BASIC EXPLORATION --------------------
print("===== Dataset Info =====")
print(f"Total rows: {dataset.shape[0]}")
print(f"Total columns: {dataset.shape[1]}")
print("Columns:", dataset.columns.tolist())

print("\n===== Null Values =====")
print(dataset.isnull().sum())

print("\n===== Sample Text Column =====")
print(dataset['content'].head(5))

# Optional: text length stats
dataset['content_length'] = dataset['content'].apply(lambda x: len(str(x)))
print("\nContent length stats:")
print(dataset['content_length'].describe())

# -------------------- CLEAN DATA --------------------
# Fill missing 'content' with empty string
dataset['content'] = dataset['content'].fillna("")

# Remove rows with missing headline
dataset = dataset[dataset['headline'].notnull()]

# Drop temporary column after stats
dataset.drop(columns=['content_length'], inplace=True)

# -------------------- SAVE CLEAN DATASET --------------------
os.makedirs("data", exist_ok=True)
dataset.to_csv(clean_file, index=False, encoding='utf-8-sig')

print(f"\n[SUCCESS] Cleaned dataset saved as {clean_file}")
print(f"Remaining rows after cleaning: {dataset.shape[0]}")