# Usage: python lidls.py
# this script scrapes prices from the Lidls website based on user input. it is implemented using bs4 and selenium; bs4 for its ease of use and selenium for its dynamic handling of of JS web content
# basic implementation atm; needs to parse all products not just featured ones

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_product_info():
    url = 'https://www.lidl.com/products?category=all&sort=productAtoZ'

    # set up selenium webdriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)

    # waiting for the product list to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.products-list"))
    )

    # get page after JS execution
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    
    search_term = input("Enter the product name or keyword to search for: ").strip().lower()
    
    # start finding matching products
    product_items = soup.select('li.grid-item') # the class li.grid-item holds the information we need
    # this was derived from manually parsing the webpage via inspect element
    matching_products = []
    
    for item in product_items: 
        h2 = item.select_one('h2') # the name
        span = item.select_one('span') # the price
        a = item.select_one('a') # the link
        if h2 and span and a and (search_term in h2.text.lower()): # checks if the name price and link exists and then if it matches our input
            # adds to the empty array a dictionary object w/ info
            matching_products.append({
                "name": h2.text,
                "price": span.text.strip(), 
                "link": a.get('href') # the info we want lies in the href
            })
    
    # final print statement
    if matching_products:
        print("Found ", len(matching_products), " products matching ", search_term, ":\n")
        for product in matching_products:
            name = product['name']
            price = product['price']
            # the price on the lidls app is given as 0.69*0.70 or 0.69* so we parse for only before the *
            price = price.split('*')[0]
            link = product['link']
            link = "https://www.lidl.com" + link # string concat
            print("Name: ", name)
            print("Price: ", price)
            print("Link: ", link, "\n")
    else:
        print("No products found matching ", search_term)        

    driver.quit()

if __name__ == '__main__':
    scrape_product_info()