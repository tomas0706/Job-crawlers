# -*- coding: utf-8 -*-
from scrapy.item import Item, Field
import scrapy

class Snagajob2NdItem(scrapy.Item):
    html_dat = Field()
    current_url = Field()
