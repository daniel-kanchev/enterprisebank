import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from enterprisebank.items import Article


class enterprisebankSpider(scrapy.Spider):
    name = 'enterprisebank'
    start_urls = ['https://www.enterprisebank.com/insights']

    def parse(self, response):
        links = response.xpath('//div[@class="insights__teaser node__content"]/a/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        if 'pdf' in response.url:
            return

        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1/span/text()').get()
        if title:
            title = title.strip()

        content = response.xpath('//div[@class="gated_content_teaser"]//text()').getall()
        content = [text for text in content if text.strip() and '{' not in text]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
