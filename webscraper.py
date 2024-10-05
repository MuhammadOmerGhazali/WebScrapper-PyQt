import undetected_chromedriver as uc
import pandas as pd 
import time
from bs4 import BeautifulSoup as bs
# Will import if needed
#from selenium.webdriver.common.by import By

# Using the default options as the base
options = uc.ChromeOptions()

# more extra options to appear more human so the driver doesnt get blcoked
options.add_argument("start-maximized")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

# iniatilzing web scraping driver
driver = uc.Chrome()

# arrays to store data
Name=[]
Price=[]
Seller=[]
Shipping=[]
Watchers=[]



def scrape(page):
    
    global Name
    global Price
    global Seller
    global Shipping
    global Watchers
    
    url = f"https://www.ebay.com/sch/i.html?_from=R40&_nkw=snacks&_sacat=0&_ipg=240&_pgn={page}"

    # navigate to the page 
    driver.get(url)
    
    #timer to wait so the page loads completely
    time.sleep(3)
    
    content = driver.page_source
    soup = bs(content, 'html.parser')
    #'s-item__etrs-text'
    for a in soup.findAll('div',attrs={'class':'s-item__info clearfix'}):
        print (a)
        name=a.find('span', attrs={'role':"heading"})
        price=a.find('span',attrs={'class':"s-item__price"})
        seller = a.findAll('span', attrs={'class': 'PRIMARY'})
        shipping=a.find('span',attrs={'class':'s-item__shipping s-item__logisticsCost'})
        #watchers=a.find('span',attrs={'class':'s-item__dynamic s-item__watchCountTotal'})
        
        if seller:
            seller_name = seller[0].text.strip()
            rating=seller[1].text.strip()
        else:
            seller_name = "Not Available"
            rating="Not Available"
        
        if name and price :
            Name.append(name.text.strip()) 
            Price.append(price.text.strip())
            Seller.append(seller_name)
            Shipping.append(shipping.text.strip() if shipping and shipping.text else "Not Available")
            Watchers.append(rating)
        else:
            print(".")
            
    df = pd.DataFrame({'Product Name':Name,'Price':Price,'Seller':Seller,'Shipping':Shipping,'Rating':Watchers})
    df.to_csv('ebay.csv', index=False, encoding='utf-8')
    

#driver code
TotalPages = 100
for page in range(1, TotalPages + 1):
    try:
        scrape(page)
        print(page)
    except Exception as e:
        print(f"Error on page {page}: {e}")
        continue

driver.quit()
print("Driver closed.")
