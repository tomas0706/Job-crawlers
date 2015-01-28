# -*- coding: utf-8 -*-
# 이 스파이더를 실행하려면 Terminal 에서 이 파일이 있는 디렉토리로 가서 "scrapy crawl snagajob1" 라는 명령어를 입력한다. 그러면 스파이더가 자동으로 데이터 크롤링을 시작할 것이다. 크롤링 된 데이터는
# pipelines.py 파일의 명령어에 따라서 mysql 데이터 베이스에 저장 될 것이다. 
# 이 스파이더를 실행하려면 scrapy 를 python 에 설치하여야 한다. (http://scrapy.org/)
# 작성일자: 2014.07.16
# 작성자: 김민

#import scrapy, urllib, re
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
import urllib
import urllib2
import re 
from snag_1st.items import Snag1StItem



#Define global variables
SPIDER_NAME = "snagajob1"
DOMAIN = "snagajob.com"

#xpath
TITLES_XPATH = '//article[@itemtype="http://schema.org/JobPosting"]'
TITLE_XPATH = "./div[1]/h2/a/text()"
URL_XPATH = "./div[1]/h2/a/@href"
LOCAL_XPATH = "./div[1]/div/span/span/span[@itemprop='addressLocality']/text()"
REGION_XPATH = "./div[1]/div/span/span/span[@itemprop='addressRegion']/text()"
COMPANY_NAME_XPATH = ".//span[@itemprop='name']/text()"




#Category url 과 Category 이름을 dict 로 만든다. 
category = dict()
category['http://www.snagajob.com/job-search/i-food+restaurant'] = 'Food & Restaurant'
category['http://www.snagajob.com/job-search/i-customer+service'] = 'Customer & Service'
category['http://www.snagajob.com/job-search/i-healthcare'] = 'Healthcare'
category['http://www.snagajob.com/job-search/i-sales+marketing'] = 'Sales & Marketing'
category['http://www.snagajob.com/job-search/i-management'] = 'Management'
category['http://www.snagajob.com/job-search/i-transportation'] = 'Transportation'
category['http://www.snagajob.com/job-search/i-personal+care+services'] = 'Personal Care & Service'
category['http://www.snagajob.com/job-search/i-warehouse+production'] = 'Warehouse & Production'
category['http://www.snagajob.com/job-search/i-automotive'] = 'Automotive'
category['http://www.snagajob.com/job-search/i-salon+spa+fitness'] = 'Salon/Spa/Fitness'
category['http://www.snagajob.com/job-search/i-hotel+hospitality'] = 'Hotel & Hospitality'
category['http://www.snagajob.com/job-search/i-installation+repair'] = 'Installation & Repair'
category['http://www.snagajob.com/job-search/i-administration+office+support'] = 'Administration & Office Support'
category['http://www.snagajob.com/job-search/i-maintenance+janitorial'] = 'Maintenance & Janitorial'



#url 에서 category 를 찾아내서 return 한다. 
def get_category(url):
	if url.find("/page") == -1:
		index = url.find("?sort=date")
		key = url[:index]
		return category[key]

	else:
		index = url.find("/page")
		key = url[:index]
		return category[key]

#Spider that crawls all the following pages starting from the start_url
class MySpider(CrawlSpider):
	name = SPIDER_NAME
	allowed_domains = [DOMAIN]

	start_urls = []
	for key in category:
		url = key + "?sort=date"
		start_urls.append(url)

#"정규표현식을 충족하는 url 만 크롤링 한다. "
	rules = (
		Rule(SgmlLinkExtractor(allow = ("/page-\d+\?sort=date", )), callback='parse_start_url', follow = True, ) , 
	)

	#start url 을 포함하여서 위의 rule 을 만족하는 페이지는 전부 크롤링 한다. 
	def parse_start_url(self, response):
		hxs = HtmlXPathSelector(response)
		titles = hxs.select(TITLES_XPATH)

		jobs = []

		for title in titles:
			job = Snag1StItem()
			current_url = response.url
			#XPATH 를 이용하여서 필요한 정보를 가져온다. 
			job["title"] = title.select(TITLE_XPATH).extract()
			job["url"] = title.select(URL_XPATH).extract()
			job["local"] = title.select(LOCAL_XPATH).extract()
			job["region"] = title.select(REGION_XPATH).extract()
			#URL 에서 CATEGORY를 가져온다. 
			job["category"] = get_category(current_url)

			job["company_name"] = title.select(COMPANY_NAME_XPATH).extract()
			jobs.append(job)
			
		#jobs 을 return 하게되면 pipelines.py에 따라 mysql 데이터베이스에 저장된다. 
		return jobs