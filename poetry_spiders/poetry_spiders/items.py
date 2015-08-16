# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PoemItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    keywords = scrapy.Field()
    text = scrapy.Field()
    region = scrapy.Field()
    author = scrapy.Field()
    year = scrapy.Field()
    period = scrapy.Field()
    classification = scrapy.Field()
    reference = scrapy.Field()
