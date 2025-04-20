# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import sqlite3


class ProductScrapPipeline:
    def __init__(self):
        db_folder = 'output'
        os.makedirs(db_folder, exist_ok=True)  # create 'output/' if it doesn't exist
        self.conn = sqlite3.connect(os.path.join(db_folder, 'products.db'))
        self.curr = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.curr.execute("""
            CREATE TABLE IF NOT EXISTS products (
            product_name TEXT DEFAULT NULL,
            price REAL DEFAULT NULL,
            product_url TEXT UNIQUE,
            rating REAL DEFAULT NULL)
        """)
        self.conn.commit()

    def process_item(self, item, spider):
        """clean price and parse to float before inserting"""
        if item['price']:
            item['price'] = item["price"].replace(',', '.').replace('$', '').replace('£', '').strip()
            try:
                item['price'] = float(item['price'])
            except ValueError:
                item['price'] = None
        else:
            item['price'] = None

        # map rating from word to int (e.g., 'Three' -> 3)
        rating_raw = item.get("rating")
        rating_map = {
            "One": 1,
            "Two": 2,
            "Three": 3,
            "Four": 4,
            "Five": 5
        }
        item["rating"] = rating_map.get(rating_raw, None)

        item["title"] = item.get("title", "").strip() or None
        item["url"] = item.get("url", "").strip() or None

        try:
            self.curr.execute("""
            INSERT OR IGNORE INTO products (product_name, price, product_url, rating)
            VALUES (?, ?, ?, ?)
            """, (item['title'], item['price'], item['url'], item['rating']))
            self.conn.commit()
        except sqlite3.IntegrityError:
            spider.logger.info(f"Duplicate item found: {item['product_url']}")
        return item

    def close_spider(self, spider):
        self.conn.close()
