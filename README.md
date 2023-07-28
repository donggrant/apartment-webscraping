# Apartments.com Scraper

This Python script uses the BeautifulSoup library to scrape data from [Apartments.com](https://www.apartments.com/). Given a city and state, it fetches apartment listings and writes them to a .csv file. Each row in the CSV file represents a single listing and includes the address of the apartment and the price.

## Dependencies

- BeautifulSoup
- requests
- pandas
- datetime

You can install these with pip:

```bash
pip install beautifulsoup4 requests pandas
```

# Usage

To use this script, you'll need to initialize an instance of the Apartments class with four parameters: `city`, `state`, `beds`, and `baths`. For example:
```python
search = Apartments("Missoula", 'MT', 4, 2)
```
This would search for four-bedroom, two-bathroom apartments in Missoula, MT.

Next, you'll want to execute the search:
```python
search.execute()
```
This will save a .csv file in the current working directory with the apartment listings.

# Output
The output .csv file is named according to the city, state, and current date. For example, a search for apartments in Missoula, MT on July 27, 2023 would generate a .csv file named "Missoula_MT_07-27-2023.csv".

Each row in the .csv file represents a single listing and includes the following columns:
- Address: The address of the apartment.
- Price: The price of the apartment. If the price is not listed, the value in this column will be "Call for Rent".
  
Please note that the script might not function as expected if the layout of Apartments.com changes significantly after the script's last update in July 2023.

# Contributing
Contributions are welcome! Please feel free to submit a pull request.

# License
This project is licensed under the terms of the MIT license.
