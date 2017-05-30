# -*- coding: utf-8 -*-
import scrapy

from .products import ProductsSpider


class CategoriesSpider(scrapy.Spider):
    name = 'categories'
    allowed_domains = ['mercadolivre.com.br']
    start_urls = ['http://mercadolivre.com.br/']

    def parse(self, response):
        base = response.css('#categories .explore-content div:last-child ul li')
        urls = base.css('a::attr(href)').extract()
        names = base.css('a::text').extract()

        categories = zip(urls, names)

        for cat in categories:
            url = cat[0]
            name = cat[1]

            spider = SubcategoriesSpider(name)
            yield scrapy.Request(url, callback=spider.parse)


class SubcategoriesSpider(scrapy.Spider):
    name = 'subcategories'
    allowed_domains = ['mercadolivre.com.br']

    def __init__(self, category):
        super(SubcategoriesSpider, self).__init__()
        self.category = category

    def parse(self, response):
        base = response.css('div.nav div ul li')

        urls = base.css('a::attr(href)').extract()
        names = base.css('a::text').extract()

        subcategories = zip(urls, names)

        for cat in subcategories:
            url = cat[0]
            name = cat[1]

            spider = ProductsSpider(self.category, name)
            yield scrapy.Request(url, callback=spider.parse)
