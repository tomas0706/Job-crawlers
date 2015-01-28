# -*- coding: utf-8 -*-


# 이 스파이더를 실행하려면 TERMINAL 로 들어가서 이 파일이 있는 디렉토리로 이동한 다음 "scrapy crawl internships1" 라고 입력한다. 그러면 자동으로 스파이더가 크롤링을 시작한다.
# pipelines.py 파일에 따라 mysql 데이터베이스에 정보가 저장된다.
# 작성일자: 2014.07.16
# 작성자: 김민 

#Import scrapy, urllib, and re  
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from internships.items import InternshipsItem
import urllib
import re 


#Defining Global Variables
SPIDER_NAME = "internships1"
DOMAIN = "internships.com"
SITE_URL = "http://www.internships.com"
URL_TMPL = '<li><a href="(/[^/=]*?)">.*</a></li>'
STARTING_URL = 'http://www.internships.com/intern'

#XPath Directory
TITLES_XPATH = '//div[@class="internship-result-item "]'
TITLE_XPATH = "./div/h3/a/text()"
URL_XPATH = "./div/h3/a/@href"


#URL을 읽어서 그 URL이 어떤 카테고리에 속하는지 알아낸다. URL 내에 카테고리가 포함되어 있다. 
def extract_category(current_url):
	index = current_url.index('?')
	# index 가 -1 이라면 첫번째 페이지이다. 
	if index == -1:
		return current_url[27:]
	# index 가 -1 아니라면 첫번째 페이지가 아니다. 
	else:
		return current_url[27:index]


#스파이더를 통해서 Internships.com 의 모든 직업 정보를 읽어온다.(1차 수집으로 address, title, category, url 만 읽어온다. 그리고 2차 수집때 이 url을 이용하여서 남어지 데이터를 수집한다.
class MySpider(CrawlSpider):
	name = SPIDER_NAME
	allowed_domains = [DOMAIN]
    
	#urllib을 이용하여서 처음 스타트 url 리스트를 만든다.
	data = urllib.urlopen(STARTING_URL)
	page = data.read()
	url_list = re.findall(URL_TMPL, page)

	#url_list 의 url 은 tuple 형식으로 되어있고 미완성이기 때문에 사이트의 url 을 붙여준다. 
	complete_url = []
	for url in url_list:
		complete = SITE_URL + str(url)
		complete_url.append(complete)
   
	start_urls = complete_url
    #스타트 url 로부터 시작하여서 page가 들어간 url은 전부 크롤링한다.
	rules = (
			Rule(SgmlLinkExtractor(allow = ("\?page=\d+", )), callback='parse_items', follow = True, ) , 
		)

#페이지가 들어간 url 은 parse하여서 xpath를 이용하여서 정보를 가져온다.
	def parse_items(self, response):
		hxs = HtmlXPathSelector(response)
		titles = hxs.select(TITLES_XPATH)
		
		jobs = []

		for title in titles:
			job = InternshipsItem()
			current_url = response.url
			job["category"] = extract_category(current_url)
			job["title"] = title.select(TITLE_XPATH).extract()
			job["url"]= title.select(URL_XPATH).extract()
			jobs.append(job)

		#jobs 를 return 하면 pipelines.py 에 따라서 자동으로 mysql 데이터베이스에 저장된다. 
		return jobs
