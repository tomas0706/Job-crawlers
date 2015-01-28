# -*- coding: utf-8 -*-

from scrapy.item import Item, Field
import scrapy


class Dice1StItem(scrapy.Item):
	skill = Field()
	url = Field()
	title = Field()
	company_name = Field()
	address = Field()
	posted_date = Field()
