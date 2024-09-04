# Njuskalo scraper

## --- Primarily scrapes real estate information --- 

## --- Work in Progress --- 

### Quick Preamble
This repo is a fork of @xxzoltanxx's scraper repo. My repo extends functionality to enable the scraping of additional listing details from real estate listings, cleans up a few bugs and removes some code that wasn't needed here. While you can still use this to scrape any category on njuskalo, the data output is meant to support real-estate listings. 

<h4>An open-source Python tool to scrape Njuskalo using Playwright and BeautifulSoup.</h4>

Use the tool at your own risk - technically, scraping is only legal if used for non-commercial purposes and if the rate of scraping is not too fast. The current scrape has preset wait times to slow down some page calls to attempt to comply. That being said, I am not responsible for any consequences or damage that may result in the use of this tool.

### Overview
The program uses Playwright to navigate Njuskalo and BeautifulSoup to parse the HTML and extract relevant data. It then saves the data in json format inside the directory of your choosing.

Run the program by running main.py

### Data output format
```
  {
    "name": NAME STRING,
    "location": LOCATION STRING,
    "Living Area": AREA STRING,
    "price": PRICE STRING,
    "link": LINK STRING,
    "published": DATE STRING,
    "coords": [
      "LAT DOUBLE",
      "LONG DOUBLE"
    ],
    "publisher": [
      "NAME STRING",
      "LINK STRING"
    ]
  },
```
  
