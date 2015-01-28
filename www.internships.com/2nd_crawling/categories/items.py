# -*- coding: utf-8 -*-
from scrapy.item import Item, Field
import scrapy

#2nd crawling 에서는 title, company_name, address, html_dat, applicatiopn_deadline, position, current_url 등의 필드를 지정한다. 
class CategoriesItem(scrapy.Item):
	title = Field()
	company_name = Field()
	address = Field()
	html_dat = Field()
	application_deadline = Field()
	position = Field()
	current_url = Field()
