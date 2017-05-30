# -*- coding: utf-8 -*-
import scrapy

from ..data.models import Product


class ProductsSpider(scrapy.Spider):
    name = 'products'
    allowed_domains = ['mercadolivre.com.br']

    def __init__(self, category, subcategory):
        super(ProductsSpider, self).__init__()
        self.category = category
        self.subcategory = subcategory

    def parse(self, response):
        base = response.css('#searchResults li div h2')
        urls = base.css('a::attr(href)').extract()

        for url in urls:
            spider = ProductSpider(self.category, self.subcategory)
            yield scrapy.Request(url, callback=spider.parse)


class ProductSpider(scrapy.Spider):
    name = 'products'
    allowed_domains = ['mercadolivre.com.br']

    def __init__(self, category, subcategory):
        super(ProductSpider, self).__init__()
        self.category = category
        self.subcategory = subcategory

    def parse(self, response):
        # avoid duplicates
        try:
            prod = Product.objects.get(url=response.url)
            self.log(f'Product already exists: {prod.name}')
        except Product.DoesNotExist:
            pass

        name = response.css('header .vip-title-main::text').extract()[0]
        name = name.replace('\n', '').replace('\t', '')

        price_main = response.css('.vip-price strong::text').extract()[0]
        price_main = ''.join(filter(lambda x: x.isdigit(), price_main))

        price_coins = response.css('.vip-price strong sup::text').extract()[0]

        price = float(f"{price_main}.{price_coins}")

        prod = Product(
            url=response.url,
            name=name,
            category=self.category,
            subcategory=self.subcategory,
            price=price
        )

        prod.save()

        self.log(f'New product saved: {prod.name}')
