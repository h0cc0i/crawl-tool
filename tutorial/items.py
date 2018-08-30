# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class PostItem(Item):
    title = Field()
    author = Field()
    entry_content = Field()
    publish_date = Field()
    image = Field()
    pass
