# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FintechdailyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    title = scrapy.Field()

    media_source = scrapy.Field()

    post_time = scrapy.Field()

    origin_url = scrapy.Field()

    post_url = scrapy.Field()
