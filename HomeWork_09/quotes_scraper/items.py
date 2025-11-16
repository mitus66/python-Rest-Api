import scrapy

class AuthorItem(scrapy.Item):
    fullname = scrapy.Field()
    born_date = scrapy.Field()
    born_location = scrapy.Field()
    description = scrapy.Field()

class QuoteItem(scrapy.Item):
    tags = scrapy.Field()
    author = scrapy.Field() # Це буде ім'я автора, яке потім зіставляється
    quote = scrapy.Field()
