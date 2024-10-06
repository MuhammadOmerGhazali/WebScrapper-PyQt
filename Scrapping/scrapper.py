import os
import undetected_chromedriver as uc
import pandas as pd
import time
from bs4 import BeautifulSoup as bs
import threading
from PyQt5.QtCore import pyqtSignal, QObject

class ScraperSignals(QObject):
    progress_signal = pyqtSignal(int)

# Initialize the web scraping driver
options = uc.ChromeOptions()
driver = uc.Chrome(options=options)

# Arrays to store data
Name = []
Price = []
Seller = []
Shipping = []
Watchers = []
Location = []
Sale = []

# Control variables
is_paused = False
current_page = 1
total_pages = 100
scrape_thread = None
scraper_signals = ScraperSignals()  # Create a signal instance

def scrape():
    global current_page, is_paused

    while current_page <= total_pages:
        if is_paused:
            time.sleep(1)
            continue

        url = f"https://www.ebay.com/sch/i.html?_from=R40&_nkw=snacks&_sacat=0&_ipg=240&_pgn={current_page}"

        try:
            driver.get(url)
            time.sleep(3)

            content = driver.page_source
            soup = bs(content, "html.parser")

            # Extract product data
            for a in soup.findAll("div", attrs={"class": "s-item__info clearfix"}):
                name = a.find("span", attrs={"role": "heading"})
                price = a.find("span", attrs={"class": "s-item__price"})
                seller = a.find("span", attrs={"class": "s-item__seller-info-text"})
                shipping = a.find("span", attrs={"class": "s-item__shipping s-item__logisticsCost"})
                location = a.find("span", attrs={"class": "s-item__location s-item__itemLocation"})
                sale = a.find("span", attrs={"class": "s-item__discount s-item__discount"})

                seller_name = seller.text.strip() if seller else "Not Available"

                if name and price:
                    Name.append(name.text.strip())
                    Price.append(price.text.strip())
                    Seller.append(seller_name)
                    Shipping.append(shipping.text.strip() if shipping and shipping.text else "Not Available")
                    Watchers.append(a.find("span", attrs={"class": "s-item__dynamic s-item__watchCountTotal"}).text.strip() if a.find("span", attrs={"class": "s-item__dynamic s-item__watchCountTotal"}) else "Not Available")
                    Location.append(location.text.strip() if location else "Not Available")
                    Sale.append(sale.text.strip() if sale else "Not Available")

            # Save progress to CSV
            csv_file_path = os.path.join(os.getcwd(), "ebay.csv")
            df = pd.DataFrame({
                "Product Name": Name,
                "Price": Price,
                "Seller": Seller,
                "Shipping": Shipping,
                "Rating": Watchers,
                "Location": Location,
                "Sale": Sale
            })
            df.to_csv(csv_file_path, index=False, encoding="utf-8")

            # Emit progress signal
            scraper_signals.progress_signal.emit(current_page)

            current_page += 1

        except Exception as e:
            print(f"Error on page {current_page}: {e}")
            continue

    print("Scraping completed.")
    driver.quit()


# Function to start/resume scraping
def start_scraping():
    global scrape_thread, is_paused

    if scrape_thread is None or not scrape_thread.is_alive():
        is_paused = False
        scrape_thread = threading.Thread(target=scrape)
        scrape_thread.start()
    else:
        is_paused = False
        print("Resuming scraping...")

# Function to pause scraping
def pause_scraping():
    global is_paused
    is_paused = True
    print("Scraping paused.")