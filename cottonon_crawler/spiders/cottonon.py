import datetime
import json

from scrapy.spiders import CrawlSpider, Spider, Request
from w3lib.url import url_query_cleaner, add_or_replace_parameters

from ..helpers import clean, detect_gender, make_rules
from ..items import CottononItem


class Mixin:
    region = 'SG'
    retailer = 'cottonon'
    allowed_domains = ['cottonon.com']

    seen_ids = set()

    default_brand = 'Cotton On'
    default_currency = ('$', 'SGD')

    one_sizes_strings = ['SOLID', 'OS']

    def return_unique_garment(self, product_id):
        if product_id in self.seen_ids:
            return None

        self.seen_ids.add(product_id)
        return CottononItem(product_id=product_id)


class CottononSGParser(Mixin, Spider):
    """
    Parsing logic for a single product (Retrieving all the metadata)
    """
    name = Mixin.retailer + '-parser'

    variation_url = 'https://cottonon.com/SG/show-variation/'

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
        product['categories'] = self.get_product_categories(response)
        product['description'] = self.get_product_description(response)
        product['gender'] = self.get_product_gender(response)
        product['image_urls'] = self.get_product_images(response)
        product['brand'] = self.get_product_brand(raw_product)
        product['currency'] = self.default_currency

        product['meta'] = self.size_requests(response, raw_product)

        return self.next_request_or_item(product)

    def parse_size_requests(self, response):
        product = response.meta['product']
        product['skus'].append(self.skus(response))

        return self.next_request_or_item(product)

    def get_product_id(self, raw_product):
        return clean(raw_product['dimension9'])

    def get_product_name(self, raw_product):
        return clean(raw_product['name'])

    def get_product_brand(self, raw_product):
        return clean(raw_product.get('brand', self.default_brand))

    def get_product_categories(self, response):
        css = '.breadcrumb-element ::text'
        return clean(response.css(css).getall())

    def get_product_description(self, response):
        css = '#details-description-container ::text'
        return clean(response.css(css).getall())

    def get_product_gender(self, response):
        categories = self.get_product_categories(response)
        return detect_gender(categories)

    def get_product_images(self, response):
        css = '.productthumbnail::attr(src)'
        images_urls = clean(response.css(css).getall())
        return [url_query_cleaner(img) for img in images_urls]

    def size_requests(self, response, raw_product):
        requests = []
        css = '.size .selectable a ::attr(data-size)'
        sizes = clean(response.css(css).getall())
        size_attr = f'dwvar_{raw_product["id"]}_size'
        color_attr = f'dwvar_{raw_product["id"]}_color'

        common_params = {
            'pid': raw_product['id'],
            'originalPid': raw_product['dimension9']
        }

        for size in sizes:
            params = common_params.copy()
            params[size_attr] = size
            params[color_attr] = raw_product['dimension9']
            url = add_or_replace_parameters(self.variation_url, params)
            requests += [Request(url, callback=self.parse_size_requests)]

        return requests

    def get_pricing_details(self, response):
        pricing = {}

        pricing['price'] = clean(response.css('.price-sales ::text').get())
        previous_price = clean(response.css('.price-standard ::text').getall())
        if previous_price:
            pricing['previous_price'] = previous_price[0]

        return pricing

    def skus(self, response):
        sku = self.get_pricing_details(response)
        size_css = '.size .selectable.selected ::attr(data-size)'
        color_css = '.color .selectable.selected ::attr(alt)'

        color = clean(response.css(color_css).getall())
        sku['color'] = color[0] if color else None
        sku['size'] = response.css(size_css).get()

        if sku['size'] in self.one_sizes_strings:
            sku['size'] = 'One Size'

        return sku

    def next_request_or_item(self, product):
        requests_queue = product['meta']
        if requests_queue:
            request = requests_queue.pop()
            request.meta.setdefault('product', product)
            yield request
        else:
            yield product


class CottononSGCrawler(Mixin, CrawlSpider):
    """
    Crawling logic for finding and hitting all the category URLs and passing over
    the control to the Parser if the parser if the product page is found
    """
    name = Mixin.retailer + '-crawler'
    start_urls = ['https://cottonon.com/SG/']
    parser = CottononSGParser()

    def __init__(self, menu_items=False):
        super().__init__()
        self.get_menu_items = bool(menu_items)
        self.menu_items = []
        self._rules = make_rules(self)

    def process_links(self, links):
        if not self.get_menu_items or not links:
            return links

        menu_links = [item['Url'] for item in self.menu_items]

        for link in links:
            category_text = clean(link.text)
            category_url = clean(link.url)

            if category_url in menu_links:
                continue

            self.menu_items.append({'Category': category_text, 'Url': category_url})

        return links
