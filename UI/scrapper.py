import os
import re
import undetected_chromedriver as uc
import pandas as pd
import time
from bs4 import BeautifulSoup as bs
import threading
from PyQt5.QtCore import pyqtSignal, QObject

class ScraperSignals(QObject):
    progress_signal = pyqtSignal(int)

options = uc.ChromeOptions()
driver = uc.Chrome(options=options)

def string_to_integer(s):
    clean_string = re.sub(r'[^0-9]', '', s)
    return int(clean_string) if clean_string else 0

def string_to_float(s):
    clean_string = re.sub(r'[^0-9.]', '', s)

    try:
        return float(clean_string) if clean_string else 0.0
    except ValueError:
        return 0.0

Productnames = []
Price = []
Miles = []
Dealername = []
Rating = []
Location = []
Reviews = []

is_paused = False
current_page = 1
total_pages = 600
scrape_thread = None
scraper_signals = ScraperSignals()  

def scrape():
    global current_page, is_paused

    while current_page <= total_pages:
        if is_paused:
            time.sleep(1)
            continue

        url = f"https://www.cars.com/shopping/results/?page={current_page}"

        try:
            driver.get(url)
            time.sleep(3)

            content = driver.page_source
            soup = bs(content, "html.parser")

            for section in soup.findAll("div", attrs={"class": "vehicle-card"}):
                productnames = section.find("h2", attrs={"class": "title"}).get_text().strip()
                price = section.find("span", attrs={"class": "primary-price"}).get_text().strip() if section.find("span", attrs={"class": "primary-price"}) else "Not found"
                miles = section.find("div", attrs={"class": "mileage"}).get_text().strip() if section.find("div", attrs={"class": "mileage"}) else "Not found"
                dealername = section.find("div", class_="dealer-name").find("strong").get_text().strip() if section.find("div", class_="dealer-name") else "Not found"
                rating = section.find("spark-rating")["rating"] if section.find("spark-rating") else "Rating not found"
                reviews = section.find('span', class_='test1 sds-rating__link sds-button-link').get_text().strip() if section.find("span", class_="test1 sds-rating__link sds-button-link") else "Reviews not found"
                location = section.find("div", class_="miles-from").get_text().strip() if section.find("div", class_="miles-from") else "Location not found"

                price = string_to_integer(price)
                miles = string_to_integer(miles)
                rating = string_to_float(rating)
                reviews = string_to_integer(reviews)

                if productnames and price:
                    Productnames.append(productnames)
                    Price.append(price)
                    Miles.append(miles)
                    Dealername.append(dealername)
                    Rating.append(rating)
                    Location.append(location)
                    Reviews.append(reviews)

            csv_file_path = os.path.join(os.getcwd(), "ebay.csv")
            df = pd.DataFrame({
                "Product Name": Productnames,
                "Price": Price,
                "Miles": Miles,
                "Dealer Name": Dealername,
                "Rating": Rating,
                "Location": Location,
                "Reviews": Reviews
            })
            df.to_csv(csv_file_path, index=False, encoding="utf-8")

            scraper_signals.progress_signal.emit(current_page)

            current_page += 1

        except Exception as e:
            print(f"Error on page {current_page}: {e}")
            continue

    print("Scraping completed.")
    driver.quit()


def start_scraping():
    global scrape_thread, is_paused

    if scrape_thread is None or not scrape_thread.is_alive():
        is_paused = False
        scrape_thread = threading.Thread(target=scrape)
        scrape_thread.start()
    else:
        is_paused = False
        print("Resuming scraping...")

def pause_scraping():
    global is_paused
    is_paused = True
    print("Scraping paused.")
