import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Create video folder
os.makedirs("data/videos", exist_ok=True)

print("🚀 Video scraper started")

# Start Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Example site with sample videos
driver.get("https://www.w3schools.com/html/html5_video.asp")
print("🌐 Website opened")

time.sleep(3)

# Collect video sources
video_links = []

# Check <video> src
videos = driver.find_elements(By.TAG_NAME, "video")
for video in videos:
    src = video.get_attribute("src")
    if src:
        video_links.append(src)

# Check <source> inside <video>
sources = driver.find_elements(By.TAG_NAME, "source")
for source in sources:
    src = source.get_attribute("src")
    if src:
        video_links.append(src)

driver.quit()

print(f"✅ Found {len(video_links)} video links")

# Download videos
for i, link in enumerate(video_links):
    try:
        print(f"👉 Downloading video {i+1}: {link}")
        response = requests.get(link, stream=True)
        file_path = os.path.join("data/videos", f"video_{i+1}.mp4")
        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print(f"✅ Saved {file_path}")
    except Exception as e:
        print(f"❌ Failed to download {link}: {e}")


