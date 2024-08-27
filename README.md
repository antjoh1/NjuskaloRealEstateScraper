# Njuskalo scraper

# -- Primarily scrapes real estate information -- 

# --- Work in Progress --- 

<h4>An open-source Python program to scrape Njuskalo using Playwright and BeautifulSoup.</h4>

Use the software provided at your own risk. I cannot be held responsible for any potential consequences, including any potential damages.
### Overview
This open-source program uses Python to scrape data from Njuskalo.hr. The program uses Playwright to navigate Njuskalo and BeautifulSoup to parse the HTML and extract relevant data. It then saves the data in json format inside the directory of your choosing.

### Installing and usage
1)Clone the repository

2)Navigate to the repository in your terminal

3)Run:
```
pip install -r requirements.txt
```

4)Run the program with
```
python main.py
```

### Data format
```
  {
    "name": "ADVERT NAME",
    "location": "LOCATION DATA" ,
    "Living area": " ## m2 "
    "Published": "DATE POSTED",
    "price": "PRICE"
  },
```

### Requirements:
- Python 3.x
- Playwright
- Streamlit
- BeautifulSoup 
  
