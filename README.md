# Njuskalo real estate scraper

## --- Work in Progress --- 

### Quick Preamble
This repo is a fork of @xxzoltanxx's scraper repo. My repo extends functionality to enable the scraping of additional listing details from real estate listings, cleans up a few bugs and removes some code that wasn't needed here. While you can still use this to scrape any category on njuskalo, the data output is meant to support real-estate listings. 

<h4>An open-source Python tool to scrape Njuskalo using Playwright and BeautifulSoup.</h4>

Use the tool at your own risk.

### Overview
The program uses Playwright to navigate Njuskalo and BeautifulSoup to parse the HTML and extract relevant data. It then saves the data in json format inside the directory of your choosing.

Run the program by running main.py - the program runs in terminal, you'll see a list of prompts that guide you to providing relevant inputs. 

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
  
