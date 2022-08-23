# Define here the models for your scraped items
from scrapy.item import Item, Field
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AppleItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    app_name = Field()
    category = Field()
    appstore_link = Field()
    img_src = Field()
