from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv
import sys

# Fix Unicode for Windows
sys.stdout.reconfigure(encoding='utf-8')

# -------------------- SETUP DRIVER --------------------
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.buzzfeed.com/")  # Change to your fake news site if needed
time.sleep(5)

# -------------------- INITIALIZE --------------------
fake_articles = []
visited_urls = set()

max_scrolls = 20      # Stop after 20 scrolls max
scroll_count = 0
target_articles = 60  # Collect at least 60 articles

# -------------------- SCROLL LOOP --------------------
while len(fake_articles) < target_articles and scroll_count < max_scrolls:
    articles = driver.find_elements(By.TAG_NAME, "a")

    for a in articles:
        try:
            url = a.get_attribute("href")
            headline = a.text.strip()

            if headline and url and len(headline) > 30 and url not in visited_urls:
                visited_urls.add(url)
                fake_articles.append((headline, url, "BuzzFeed", "FAKE"))

            if len(fake_articles) >= target_articles:
                break
        except:
            continue

    # Visible scroll
    driver.execute_script("window.scrollBy(0, 2000);")
    time.sleep(1)
    scroll_count += 1

print(f"✅ Collected {len(fake_articles)} fake articles after {scroll_count} scrolls")

# -------------------- OPTIONAL: FETCH CONTENT (SLOW) --------------------
# Uncomment below if you want full content, else skip to save CSV
"""
for i in range(len(fake_articles)):
    headline, url, source, label = fake_articles[i]

    try:
        driver.get(url)
        time.sleep(2)

        paragraphs = driver.find_elements(By.TAG_NAME, "p")
        content = " ".join([p.text for p in paragraphs if p.text])

        fake_articles[i] = (headline, url, content, source, label)
    except:
        fake_articles[i] = (headline, url, "", source, label)
"""

# -------------------- SAVE TO CSV --------------------
with open("fake_news_articles.csv", "w", newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["headline", "url", "source", "label"])
    for row in fake_articles:
        writer.writerow(row)

print("✅ Data saved to fake_news_articles.csv")
input("Press Enter to close...")
driver.quit()