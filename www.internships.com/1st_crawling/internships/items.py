# -*- coding: utf-8 -*-
from scrapy.item import Item, Field
import scrapy

#1st_crawling 에서는 category, title, url 만 크롤링 한다.
class InternshipsItem(scrapy.Item):
	category = Field()
	title = Field()
	url = Field()
