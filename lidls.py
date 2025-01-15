# Usage: python lidls.py
# this script scrapes product name, prices, links, and images from the Lidls website based on user input. it is implemented using bs4 and selenium; bs4 for its ease of use and selenium for its interaction with web content
# doesn't account for lidl deals
# parse for item weight ? 

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_product_info():
    # set up selenium webdriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    driver.get('https://www.lidl.com/')

    # click the search button to change web content
    search_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "search-input"))
    )

    search_btn.click()

    # wait until the "new" input has appeared
    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "MuiInputBase-input"))
    )

    # parse user input
    search_term = input("Enter the product name or keyword to search for: ").strip().lower()
    search_input.send_keys(search_term)
    search_input.submit() # hits enter

    time.sleep(2) # wait for page to reload

    # waiting for the product list to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "pagination-grid"))
    )

    # get page after JS execution
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # start finding matching products
    product_items = soup.select('li.grid-item') # the class li.grid-item holds the information we need
    matching_products = []
    
    for item in product_items: 
        h2 = item.select_one('h2') # the name
        span = item.select_one('span') # the price
        a = item.select_one('a') # the link
        img = item.select_one('img') # the image link
        if h2 and span and a and (search_term in h2.text.lower()): # checks if the name price and link exists and then if it matches our input
            # adds to the empty array a dictionary object w/ info
            matching_products.append({
                "name": h2.text.strip(),
                "price": span.text.strip().split('*')[0], # use only the first part before *
                "link": "https://www.lidl.com" + a.get('href'), # the info we want lies in the href
                "image": img.get('src')
            })

    # basic sort function by lowest price
    def get_price(product):
        return product['price']
        
    matching_products.sort(key=get_price)

    # final print statement
    if matching_products:
        print("Found", len(matching_products), "products matching", search_term, ":\n")
        for product in matching_products:
            print("Name:", product['name'])
            print("Price:", product['price'])
            print("Link:", product['link'])
            print("Image:", product['image'], "\n")
    else:
        print("No products found matching", search_term)        

    driver.quit()

if __name__ == '__main__':
    scrape_product_info()