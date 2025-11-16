import scrapy
from ..items import QuoteItem, AuthorItem # Імпортуємо Items

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    # Додаємо Items до класу павука для зручності доступу в пайплайні
    AuthorItem = AuthorItem
    QuoteItem = QuoteItem

    def parse(self, response):
        # Парсинг цитат
        for quote_div in response.css('div.quote'):
            quote_item = QuoteItem()
            quote_item['tags'] = quote_div.css('div.tags a.tag::text').getall()
            quote_item['author'] = quote_div.css('small.author::text').get()
            quote_item['quote'] = quote_div.css('span.text::text').get().strip() # Видаляємо зайві пробіли
            yield quote_item

            # Переходимо на сторінку автора для збору додаткової інформації
            author_url = quote_div.css('small.author + a::attr(href)').get()
            if author_url:
                yield response.follow(author_url, self.parse_author)

        # Перехід на наступну сторінку
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_author(self, response):
        # Парсинг інформації про автора
        author_item = AuthorItem()
        author_item['fullname'] = response.css('h3.author-title::text').get().strip()
        author_item['born_date'] = response.css('span.author-born-date::text').get().strip()
        author_item['born_location'] = response.css('span.author-born-location::text').get().strip()
        author_item['description'] = response.css('div.author-description::text').get().strip()
        yield author_item
