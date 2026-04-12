from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import sys

# Fix Unicode output on Windows
sys.stdout.reconfigure(encoding='utf-8')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 10)

# Use list of tuples (headline, source, label)
all_headlines = []

# -------------------- BBC --------------------
driver.get("https://www.bbc.com/news")
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h2, h3")))

bbc_headlines = driver.find_elements(By.CSS_SELECTOR, "h2, h3")
for h in bbc_headlines:
    try:
        text = h.text.strip()
        if text and len(text) > 20:
            all_headlines.append((text, "BBC", "REAL"))
    except:
        continue

print(f"BBC collected: {len(all_headlines)}")

# -------------------- NDTV --------------------
driver.get("https://www.ndtv.com/latest")
wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "h2")))

ndtv_headlines = driver.find_elements(By.TAG_NAME, "h2")
for h in ndtv_headlines:
    try:
        text = h.text.strip()
        if text and len(text) > 20:
            all_headlines.append((text, "NDTV", "REAL"))
    except:
        continue

print(f"After NDTV: {len(all_headlines)}")

# -------------------- Hacker News --------------------
driver.get("https://news.ycombinator.com/")
wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "titleline")))

hn_headlines = driver.find_elements(By.CLASS_NAME, "titleline")
for h in hn_headlines:
    try:
        text = h.text.strip()
        if text and len(text) > 10:
            all_headlines.append((text, "HackerNews", "REAL"))
    except:
        continue

print(f"After HackerNews: {len(all_headlines)}")

# -------------------- SAVE TO CSV --------------------
with open("news_datafinal.csv", "w", newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["headline", "source", "label"])
    for headline, source, label in all_headlines:
        writer.writerow([headline, source, label])

print("\nData saved to news_data.csv")
input("Press Enter to close...")
driver.quit()