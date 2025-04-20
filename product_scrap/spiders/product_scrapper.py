import scrapy
from urllib.parse import urljoin


class ProductScrapperSpider(scrapy.Spider):
    name = 'product_scrapper'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']  # adjust starting URL

    def parse(self, response):
        """using the css selectors method to scrape the products"""
        books = response.css("article.product_pod")
        """iterate over items and send the item to pipeline for cleaning and saving"""
        for book in books:
            yield {
                "title": book.css("h3 a::attr(title)").get(),
                "price": book.css(".price_color::text").get(),
                "rating": book.css("p.star-rating").attrib["class"].split()[-1],
                "url": urljoin(response.url, book.css("h3 a::attr(href)").get()),
            }

        # handle pagination
        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
