import json
import datetime

from scrapy.link import Link
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule, Spider
from w3lib.url import url_query_cleaner

from ..items import CottononItem


class Mixin:
    region = 'SG'
    retailer = 'cottonon'
    allowed_domains = ['cottonon.com']

    seen_ids = set()

    def return_unique_garment(self, product_id):
        if product_id in self.seen_ids:
            return None

        self.seen_ids.add(product_id)
        return CottononItem(product_id=product_id)


class CottononSGParser(Mixin, Spider):
    name = Mixin.retailer + '-parser'

    def raw_product(self, response):
        css = '.primary-content script ::text'
        raw_data = response.css(css).re_first('dataLayerArr = \[({.*})\];')
        return json.loads(raw_data)['ecommerce']['detail']['products'][0]

    def default_product(self, product, response):
        product['url'] = response.url
        product['datetime'] = datetime.datetime.now().__str__()
        product['skus'], product['image_urls'] = [], []

    def parse(self, response, **kwargs):
        raw_product = self.raw_product(response)
        product_id = self.get_product_id(raw_product)

        product = self.return_unique_garment(product_id)
        if not product:
            return

        self.default_product(product, response)
        product['name'] = self.get_product_name(raw_product)

        yield product

    def get_product_id(self, raw_product):
        return raw_product['id']

    def get_product_name(self, raw_product):
        return raw_product['name']


class CottononSGCrawler(Mixin, CrawlSpider):
    name = Mixin.retailer + '-crawler'
    start_urls = ['https://cottonon.com/SG/']
    parser = CottononSGParser()

    deny_re = [
        '/stationery/',
        '/stationery-homewares/',
        '/collab-shop/',
        '/tech-accessories/',
        '/sale-tech/',
        '/sale-gifting/',
        '/sale-stationery-living/',
        '/gifts/',
        '-gifts',
    ]

    listings_css = [
        '.top-level-container .menu-item',
        '.page-next'
    ]

    product_css = ['.thumb-link']

    def process_links(self, links):
        return [Link(url=url_query_cleaner(link.url)) for link in links]

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css, deny=deny_re), callback='_parse'),
        Rule(LinkExtractor(restrict_css=product_css), callback=parser.parse, process_links='process_links'),
    )

