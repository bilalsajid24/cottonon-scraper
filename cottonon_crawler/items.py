from scrapy.item import Item, Field


class CottononItem(Item):
    meta = Field(default='')
    product_id = Field()
    datetime = Field()
    url = Field()
    name = Field()
    description = Field()
    categories = Field()
    gender = Field()
    brand = Field()
    price = Field()
    currency = Field()
    image_urls = Field()
    skus = Field()
    out_of_stock = Field()
