import json
import os

class JsonWriterPipeline:
    def open_spider(self, spider):
        self.authors_file = open('authors.json', 'w', encoding='utf-8')
        self.quotes_file = open('quotes.json', 'w', encoding='utf-8')
        self.authors_data = []
        self.quotes_data = []

    def close_spider(self, spider):
        json.dump(self.authors_data, self.authors_file, ensure_ascii=False, indent=2)
        json.dump(self.quotes_data, self.quotes_file, ensure_ascii=False, indent=2)
        self.authors_file.close()
        self.quotes_file.close()
        print("\nScraping finished. Data saved to authors.json and quotes.json.")

    def process_item(self, item, spider):
        if isinstance(item, spider.AuthorItem):
            # Перевіряємо, чи автор вже був доданий, щоб уникнути дублікатів
            if item not in self.authors_data: # Порівняння за вмістом Item
                self.authors_data.append(dict(item))
        elif isinstance(item, spider.QuoteItem):
            self.quotes_data.append(dict(item))
        return item
