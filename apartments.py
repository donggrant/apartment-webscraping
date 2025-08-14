from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
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
        self.url = self.build_url()
        self.data = {}
        self.date = datetime.now().strftime("%m-%d-%Y")

    def build_url(self):
        return "https://www.apartments.com/" + '-'.join(self.city.lower().split(' ')) + '-' + self.state.lower() + '/'

    def print_query(self):
        print("Location of Interest:", self.city + ", " + self.state)
        print("Number of Beds:", self.beds)
        print("Number of Baths:", self.baths)

    def fetch_html(self, url):
        try:
            response = requests.get(url, headers=HEADERS)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("Something went wrong", err)

    def get_listings(self):
        main_page_html = self.fetch_html(self.url)
        if main_page_html is None:
            return None
        page_range_element = main_page_html.find('span', class_="pageRange")
        try:
            page_range = int(page_range_element.text.split(' ')[-1]) if page_range_element else 1
        except (ValueError, AttributeError):
            page_range = 1
        listings = []
        for i in range(1, page_range + 1):
            page_html = self.fetch_html(self.url + str(i) + "/")
            if page_html:
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
        listings = self.get_listings()
        if listings is None:
            print("Oops, this place doesn't exist or has no results.")
            return
        self.data["address"] = [self.get_address(listing) for listing in listings]
        self.data["price"] = [self.get_prices(listing) for listing in listings]
        pd.DataFrame(self.data).to_csv(self.city.replace(' ', '_')
                                       + "_" + self.state
                                       + "_" + self.date
                                       + ".csv", index=False)


search = Apartments("Missoula", 'MT', 4, 2)
search.print_query()
search.execute()
