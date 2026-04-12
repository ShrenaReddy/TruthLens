import pandas as pd

df = pd.read_csv("data/news_dataset.csv")

# Show first 5 rows
print(df.head())

# Show dataset shape
print(df.shape)

# Optional: Check columns to confirm
print("\nColumns:", df.columns)