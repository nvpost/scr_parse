import numpy as np
import scrapy
import re


class OwenSpider(scrapy.Spider):
    custom_settings = {'FEED_URI': 'results/owen.csv'}

    name = 'owen'

    """ Составляем корректный список страниц. """
    allowed_domains = ['https://owen.ru/']
    first_page = ['https://owen.ru/catalog']

    """ Вставлем на 1 меcто (0 индекс) нашу первую страницу. """
    start_urls = first_page

    def refine(self, string, field):
        compiled = re.compile('<.*?>')
        clean = re.sub(compiled, '|', string)
        clean = clean.strip('').replace('\t', '').replace('\n', '').replace('\xa0', '')
        amount = abs(int(clean.split('|')[field]))
        return amount

    def parse(self, response):
        products = {}
        url_list = response.xpath("//li[@class='catalog-page-group__item']//a/@href").extract()
        title_list = response.xpath("//li[@class='catalog-page-group__item']//a/text()").extract()

        url_list = ['https:'+url for url in url_list]

        for i in range(len(url_list)):
            scrapy.Request(url_list[i], self.parse)

            product_title_list = response.xpath("//span[@class='product-card__label-wrapper']//span/text()").extract()
            dirty_product_price_list = response.xpath("//div[@class='product-card__price']//span/text()").extract()
            product_price_list = []
            rub = dirty_product_price_list[::2]
            koop = dirty_product_price_list[1::2]
            for p in range(len(rub)):
                product_price_list.append((rub[p]+koop[p]).replace(" ", ""))

            imgs = response.xpath("//a[@class='product-card__image']//img/@src").extract()

            imgs_list = ['https://owen.ru' + img for img in imgs]
            category_row=[]
            for prod in  range(len(product_title_list)):
                row = {
                    'category_label': title_list[i],
                    'category_url': url_list[i],
                    'product_label': product_title_list[prod],
                    'product_price': product_price_list[prod],
                    'product_img': imgs_list[prod]
                }
                category_row.append(row)
                yield row
            print(category_row)




        #print('url_list', url_list)


        # for item in zip(clean_titles, clean_prices, clean_old_prices, clean_discounts, imgs):
        #     scraped_info = {
        #         'title': item[0],
        #         'price': item[1],
        #         'old_price': item[2],
        #         'discount_offer': item[3],
        #         'image_urls': [item[4]]}
        #     yield scraped_info