# data_scraper.py
# Scrapes quotes (text), authors, and author images from quotes.toscrape.com
print("this is original file")

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time, os, requests, json

print("Script started ✅")

# --- Setup driver ---
print("Launching Chrome...")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

print("Opening website...")
driver.get("https://quotes.toscrape.com/")
print("Website loaded ✅ Title:", driver.title)

time.sleep(2)  # let page load

# --- Prepare storage ---
os.makedirs("data/images", exist_ok=True)
quotes_data = []

# --- Scraping loop ---
while True:
    print("Scraping a page...")

    quotes = driver.find_elements(By.CLASS_NAME, "quote")

    for quote in quotes:
        text = quote.find_element(By.CLASS_NAME, "text").text
        author = quote.find_element(By.CLASS_NAME, "author").text

        # Some authors have profile images
        try:
            img = quote.find_element(By.XPATH, "..//img").get_attribute("src")
        except:
            img = None

        quotes_data.append({"text": text, "author": author, "img": img})

        # download image if available
        if img:
            img_name = f"data/images/{author}.jpg"
            if not os.path.exists(img_name):
                try:
                    img_content = requests.get(img).content
                    with open(img_name, "wb") as f:
                        f.write(img_content)
                    print(f"Downloaded image for {author}")
                except Exception as e:
                    print(f"Failed to download image: {e}")

    # go to next page if exists
    try:
        next_btn = driver.find_element(By.LINK_TEXT, "Next →")
        print("Moving to next page...")
        next_btn.click()
        time.sleep(2)
    except:
        print("No more pages found 🚀")
        break

driver.quit()

# --- Save text data ---
with open("data/quotes.json", "w", encoding="utf-8") as f:
    json.dump(quotes_data, f, ensure_ascii=False, indent=2)

print("Scraping done ✅ Data saved in data/quotes.json + images/")

