import csv
import os
import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .utils import GENDER_MAP, Gender


def open_category_file():
    csv_file = open(os.environ['FILE_PATH'], newline='')
    return csv.DictReader(csv_file)


def remove_spaces_and_strip(value):
    return re.sub(r'\s+', ' ', value.replace('\xa0', ' ')).strip()


def clean(lst_or_str):
    if isinstance(lst_or_str, list):
        return [x for x in (remove_spaces_and_strip(y) for y in lst_or_str if y is not None) if x]

    return remove_spaces_and_strip(lst_or_str)


def detect_gender(str_or_lst):
    detected_genders = []
    if isinstance(str_or_lst, list):
        str_or_lst = ' '.join(str_or_lst)

    for key, gender in GENDER_MAP.items():
        if key in str_or_lst.lower():
            detected_genders.append(gender)

    # Looping through genders (Enum) for returning on the basis of order
    for gender in Gender:
        if gender.value in detected_genders:
            return gender.value

    # Return default gender value
    return Gender.ADULTS.value


def make_rules(crawler):
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

    listings_css = ['.top-level-container .menu-item']
    pagination_css = ['.page-next']
    product_css = ['.thumb-link']

    rules = [
        Rule(LinkExtractor(restrict_css=listings_css, deny=deny_re), process_links=crawler.process_links),
    ]

    if crawler.read_from_file:
        rules = []

    if not crawler.get_menu_items or crawler.read_from_file:
        rules += [
            Rule(LinkExtractor(restrict_css=pagination_css, deny=deny_re)),
            Rule(LinkExtractor(restrict_css=product_css), callback=crawler.parser.parse),
        ]

    return rules
