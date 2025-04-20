# Web Scraping & Data Processing Task
## Choice of Scrapy Framework

Scrapy was selected for this project due to its robust architecture specifically designed for web scraping. Its built-in components like Spiders, Items, and Pipelines provide a clear and organized structure for efficient data extraction (product name, price, URL, rating) and processing. Scrapy's powerful CSS and XPath selectors enable precise targeting of information within the website's HTML. Furthermore, my prior experience with Scrapy allows for faster and more confident development, leveraging existing knowledge of its core concepts, data handling, and pagination management to deliver a reliable and effective scraping solution.

## Overview

This project is a Scrapy spider that scrapes book information (title, price, rating, and URL) from [Books to Scrape](http://books.toscrape.com), a site made for practicing web scraping.

All scraped data is cleaned and stored in a local SQLite database.

---

## ✅ Features

- Scrapes all book listings from every page
- Extracts:  
  - Product name  
  - Price  
  - Rating  
  - Product URL  
- Cleans price and rating fields
- Saves data into a SQLite database (`output/products.db`)

---

## ⚙️ Setup Instructions
Make sure you have python installed in your machine. I am using the python 3.10

### 1. Create a Virtual Environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
You can skip this part and just run 
```bash
pip install -r requirements.txt
```

### 2. Run spider and crawl data
You can now run the spider. Just run this command in the terminal:
```bash
scrapy crawl product_scrapper
```

### 3. Check data
Your data will be saved in database. You can view data in any SQLite viewer or CLI tool:
```bash
sqlite3 output/products.db
```
and then run:
```bash
SELECT * FROM products;
```

### 4. (Optional) Save data in other format
If you want to save in  json/csv format, run this command
```bash
scrapy crawl product_scrapper -o products.json
```

## Notes
 - Website might block the request if we keep on scrapping data from their server.
-  Scrapy does handle the concurrency via the settings. I have set the settings to 10.
```bash
# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 10
```
## Future Improvements
- I have not used the proxy/user-agent rotations in this project, we can implement it once needed.
- I have used SQLite database (since dataset is small and we need just 1 table to save it). We can update it to use any other database if we need multiple tables to store data and data amount in big.