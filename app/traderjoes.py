from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def traderjoes(search_term):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    driver.get('https://www.traderjoes.com/home/products')

    search_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "HeroBannerProductsSearch_heroBannerProductsSearch__wrapper__3GvXQ"))
    )

    search_btn.click()

    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "SearchField_searchField__inputText__2IH6E"))
    )
    search_input.send_keys(search_term) 
    search_input.submit()

    time.sleep(2)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "SearchResults_searchResults__CEWwK"))
    )

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    product_items = soup.select('article.SearchResultCard_searchResultCard__3V-_h')
    matching_products = []

    for item in product_items: 
        h3 = item.select_one('h3') # the name
        a = item.select_one('a') # the link
        span = item.select_one('span.ProductPrice_productPrice__price__3-50j') # the price
        if h3 and span and a and (search_term in h3.text.lower()):
            matching_products.append({
                "name": h3.text.strip(),
                "price": span.text.strip(),
                "link": "https://www.traderjoes.com" + a.get('href'),
            })
    
    def get_price(product):
        return product['price']
        
    matching_products.sort(key=get_price)

    n = len(matching_products)

    if matching_products:
        print("Found", len(matching_products), "products matching", "eggs", "\n")
        for i in range(n):
            print ("Name:", matching_products[i]['name'])
            print ("Price:", matching_products[i]['price'])
            print ("Link:", matching_products[i]['link'])
    else:
        print("No products found matching", search_term)

    driver.quit()
    return matching_products

if __name__ == '__main__':
    traderjoes()