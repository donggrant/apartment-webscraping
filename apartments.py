from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime

HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15",
        "Accept": "test/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-gb",
        "Accept-Encoding": "br, gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
        "Referer": "http://www.google.com/",
    }

class Apartments:

    def __init__(self, city, state, beds, baths):
        self.city = city
        self.state = state
        self.beds = beds
        self.baths = baths
        self.url = "https://www.apartments.com/" + '-'.join(self.city.lower().split(' ')) + '-' + self.state.lower() + '/'
        self.data = {}
        self.date = datetime.now().strftime("%m-%d-%Y")
    
    def print_query(self):
        print("Location of Interest:", self.city + ", " + self.state)
        print("Number of Beds:", self.beds)
        print("Number of Baths:", self.baths)

    def get_listings(self):
        main_page = requests.get(self.url, headers=HEADERS)
        print(main_page) # if not a 200 response, need to update headers
        main_page_html = BeautifulSoup(main_page.content, 'html.parser')
        page_range = main_page_html.find('span', class_="pageRange").text.split(' ')[-1]
        listings = []
        for i in range(1, int(page_range) + 1):
            page = requests.get(self.url + str(i) + "/", headers=HEADERS)
            page_html = BeautifulSoup(page.content, 'html.parser')
            listings += page_html.find_all('li', class_="mortar-wrapper")
        return listings
    
    def get_address(self, listing):
        element1 = listing.find('div', class_="property-address js-url")
        element2 = listing.find('p', class_="property-address js-url")
        if element1:
            return element1.text
        if element2:
            return element2.get('title')

    def get_prices(self, listing):
        element1 = listing.find('p', class_="property-pricing")
        element2 = listing.find('div', class_="price-range")
        element3 = listing.find('span', class_="property-rents")
        if element1:
            return element1.text
        if element2:
            return element2.text
        if element3:
            return element3.text
        return "Call for Rent"

    def execute(self):
        listings = search.get_listings()
        self.data["address"] = [search.get_address(listing) for listing in listings]
        self.data["price"] = [search.get_prices(listing) for listing in listings]
        pd.DataFrame(self.data).to_csv(self.city.replace(' ', '_')
            + "_" + self.state
            + "_" + self.date
            + ".csv", index = False)

search = Apartments("Manhattan", 'NY', 2, 1)
search.print_query()
search.execute()