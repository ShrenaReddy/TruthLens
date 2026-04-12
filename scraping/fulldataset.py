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

# Store tuples: (headline, url, content, source, label)
all_articles = []

# -------------------- BBC --------------------
driver.get("https://www.bbc.com/news")
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href*='/news/']")))

links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/news/']")
bbc_urls = set()  # avoid duplicates

for link in links:
    try:
        url = link.get_attribute("href")
        headline = link.text.strip()
        if headline and url and len(headline) > 20 and url not in bbc_urls:
            bbc_urls.add(url)
            all_articles.append((headline, url, "", "BBC", "REAL"))
    except:
        continue

print(f"BBC articles collected: {len(bbc_urls)}")

# -------------------- NDTV --------------------
driver.get("https://www.ndtv.com/latest")
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href*='news']")))

links = driver.find_elements(By.CSS_SELECTOR, "a[href*='news']")
ndtv_urls = set()

for link in links:
    try:
        url = link.get_attribute("href")
        headline = link.text.strip()
        if headline and url and len(headline) > 20 and url not in ndtv_urls:
            ndtv_urls.add(url)
            all_articles.append((headline, url, "", "NDTV", "REAL"))
    except:
        continue

print(f"NDTV articles collected: {len(ndtv_urls)}")

# -------------------- Hacker News --------------------
driver.get("https://news.ycombinator.com/")
wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "titleline")))

hn_links = driver.find_elements(By.CLASS_NAME, "titleline")
hn_urls = set()

for h in hn_links:
    try:
        a_tag = h.find_element(By.TAG_NAME, "a")
        url = a_tag.get_attribute("href")
        headline = a_tag.text.strip()
        if headline and url and len(headline) > 10 and url not in hn_urls:
            hn_urls.add(url)
            all_articles.append((headline, url, "", "HackerNews", "REAL"))
    except:
        continue

print(f"HackerNews articles collected: {len(hn_urls)}")

# -------------------- EXTRACT FULL CONTENT --------------------
def get_article_content(url, source):
    """Visit the article URL and extract main text depending on source"""
    try:
        driver.get(url)
        time.sleep(2)  # small wait for page load
        if source == "BBC":
            paragraphs = driver.find_elements(By.CSS_SELECTOR, "article p")
        elif source == "NDTV":
            paragraphs = driver.find_elements(By.CSS_SELECTOR, ".storyText p")
        elif source == "HackerNews":
            # HackerNews links are often external, skip content
            return ""
        else:
            return ""

        content = " ".join([p.text for p in paragraphs if p.text])
        return content
    except:
        return ""

# Update all_articles with content
for i in range(len(all_articles)):
    headline, url, _, source, label = all_articles[i]
    content = get_article_content(url, source)
    all_articles[i] = (headline, url, content, source, label)

# -------------------- SAVE TO CSV --------------------
with open("news_articles.csv", "w", newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["headline", "url", "content", "source", "label"])
    for article in all_articles:
        writer.writerow(article)

print("\nData saved to news_articles.csv")
input("Press Enter to close...")
driver.quit()