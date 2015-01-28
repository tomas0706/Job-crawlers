# -*- coding: utf-8 -*-
#이 스파이더를 실행하려면 TERMINAL 로 들어가서 이 파일이 있는 디렉토리로 이동한 다음 "dice1" 라고 입력한다. 그러면 자동으로 스파이더가 크롤링을 시작한다.
# 이 스파이더를 실행하려면 scrapy 를 python 에 설치하여야 한다. (http://scrapy.org/)
# 작성일자: 2014.07.16
# 작성자: 김민


#import scrapy, dice, urllib, and re
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from dice_1st.items import Dice1StItem
import urllib
import urllib2
import re 

#Global variables
SPIDER_NAME = "dice1"
DOMAIN = "dice.com"
URL_TMPL = '<a class="primary" href="(.*?)">(.*?)</a>'
CATEGORY_URL = 'http://www.dice.com/job/browse/skill.html'
PAGE_TMPL = "http://www.dice.com/job/results/.*?\?o=\d+&x=all&p=k"

#XPath
RESTRICT_XPATH = '//a[@class="nextPage"]'
TITLES_XPATH = '//tr'
URL_XPATH = './td[1]/div/a/@href'
TITLE_XPATH = './td[1]/div/a/text()'
COMPANY_NAME_XPATH = './td[2]/a/text()'
ADDRESS_XPATH = './td[3]/a/text()'
POSTED_DATE_XPATH = './td[4]/text()'



#url 에서 skill 을 찾아내서 return 한다. 
def get_skill(url):
	first_index = url.find("/job/results/")
	last_index = url.find("?")
	return url[first_index + 13 : last_index]


class MySpider(CrawlSpider):
	data = urllib2.urlopen(CATEGORY_URL)
	page = data.read()
	url_list = re.findall(URL_TMPL, page)

	name = SPIDER_NAME
	allowed_domains = [DOMAIN]

	start_urls = []
	for key in url_list:
		url = key[0]
		start_urls.append(url)

	#이 룰에 따라서 크롤링 한다. 	
	rules = (
			Rule(SgmlLinkExtractor(allow = (PAGE_TMPL, ), restrict_xpaths = (RESTRICT_XPATH, )), callback='parse_start_url', follow = True, ) , 
		)

	def parse_start_url(self, response):
		hxs = HtmlXPathSelector(response)
		titles = hxs.select(TITLES_XPATH)

		jobs = []		

		for title in titles:
			job = Dice1StItem()
			current_url = response.url

			job["skill"] = get_skill(current_url)
			
			#XPATH 를 이용하여서 데이터를 가져온다. 
			job["url"] = title.select(URL_XPATH).extract()
			job["title"] = title.select(TITLE_XPATH).extract()
			job["company_name"] = title.select(COMPANY_NAME_XPATH).extract()
			job["address"] = title.select(ADDRESS_XPATH).extract()
			job["posted_date"] = title.select(POSTED_DATE_XPATH).extract()
			jobs.append(job)

		return jobs

