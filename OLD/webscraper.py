# scrapper.py

import os
import undetected_chromedriver as uc
import pandas as pd
import time
from bs4 import BeautifulSoup as bs
import threading

# Initialize the web scraping driver
options = uc.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode (optional)
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

# Define a callback function for progress updates
def progress_callback(current, total):
    # This function can be used to update the progress in the UI
    print(f"Progress: {current}/{total} pages scraped.")

def scrape():
    global current_page, is_paused

    while current_page <= total_pages:
        if is_paused:
            time.sleep(1)  # Wait until the process is resumed
            continue

        url = f"https://www.ebay.com/sch/i.html?_from=R40&_nkw=snacks&_sacat=0&_ipg=240&_pgn={current_page}"

        try:
            # Navigate to the page
            driver.get(url)

            # Timer to wait so the page loads completely
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

                if seller:
                    seller_name = seller.text.strip()
                else:
                    seller_name = "Not Available"

                if name and price:
                    Name.append(name.text.strip())
                    Price.append(price.text.strip())
                    Seller.append(seller_name)
                    Shipping.append(shipping.text.strip() if shipping and shipping.text else "Not Available")
                    Watchers.append(a.find("span", attrs={"class": "s-item__dynamic s-item__watchCountTotal"}).text.strip() if a.find("span", attrs={"class": "s-item__dynamic s-item__watchCountTotal"}) else "Not Available")
                    Location.append(location.text.strip() if location else "Not Available")
                    Sale.append(sale.text.strip() if sale else "Not Available")

            # Save progress to CSV after each page in the current working directory
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

            # Emit progress update
            progress_callback(current_page, total_pages)

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
