# -*- coding: utf-8 -*-

from scrapy.item import Item, Field
import scrapy



class Snag1StItem(scrapy.Item):
	category = Field()
	url = Field()
	local = Field()
	region = Field()
	company_name = Field()
	title = Field()
