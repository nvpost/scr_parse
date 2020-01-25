# -*- coding: utf-8 -*-
import scrapy


class OwenSpiderSpider(scrapy.Spider):
    name = 'owen_spider'
    allowed_domains = ['https://owen.ru/catalog']
    start_urls = ['http://https://owen.ru/catalog/']

    def parse(self, response):
        pass
