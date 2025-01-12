#Config selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument(" - headless") # Run browser in the background
driver = webdriver.Chrome(service=Service(), options=options)
driver.get("https://www.google.com/maps")

#Navigate to google maps
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
try:
    accept_button = driver.find_element(By.CSS_SELECTOR, "[aria-label='Accept all']")
    accept_button.click()
except NoSuchElementException:
    print("No GDPR requirements detected")

#Submit a search
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
search_box = WebDriverWait(driver, 10).until(
EC.presence_of_element_located((By.CSS_SELECTOR, "#searchboxinput"))
)
search_box.send_keys("restaurants columbus ohio")
search_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Search']")
search_button.click()

#Extract business data
business_items = WebDriverWait(driver, 30).until(
EC.presence_of_all_elements_located((By.XPATH, '//div[@role="feed"]//div[contains(@jsaction, "mouseover:pane")]'))
)

#Extract basic details
for item in business_items:
    name = item.find_element(By.CSS_SELECTOR, "div.fontHeadlineSmall").text
    link = item.find_element(By.CSS_SELECTOR, "a[jsaction]").get_attribute("href")
print(f"Business: {name}, Link: {link}")

#Extract Reviews and ratings
#import re
#reviews_element = item.find_element(By.CSS_SELECTOR, "span[role='img']")
#reviews_text = reviews_element.get_attribute("aria-label")
#match = re.match(r"(\d+\.\d+) stars (\d+[,]*\d+) Reviews", reviews_text)
#if match:
    #stars = float(match.group(1))
    #review_count = int(match.group(2).replace(",", ""))
#print(f"Stars: {stars}, Reviews: {review_count}")

#Extract additional info
#info_div = item.find_element(By.CSS_SELECTOR, ".fontBodyMedium")
#spans = info_div.find_elements(By.XPATH, ".//span[not(@*) or @style]")
#details = [span.text for span in spans if span.text.strip()]
#print("Details:", details)

#Save data to CSV
data = []
for item in business_items:
    # Collect data as shown above and append to a list
    data.append({
    "name": name,
    "link": link,
    #"stars": stars,
})

#Write to CSV
import csv
with open("business_data.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)