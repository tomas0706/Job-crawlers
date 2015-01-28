# -*- coding: utf-8 -*-
# 이 스파이더를 실행하려면 Terminal 에서 이 파일이 있는 디렉토리로 가서 "scrapy crawl internships2" 라는 명령어를 입력한다. 그러면 스파이더가 자동으로 데이터 크롤링을 시작할 것이다. 크롤링 된 데이터는
# pipelines.py 파일의 명령어에 따라서 mysql 데이터 베이스에 저장 될 것이다. 
# 이 스파이더를 실행하려면 scrapy 를 python 에 설치하여야 한다. (http://scrapy.org/)
# 작성일자: 2014.07.16
# 작성자: 김민


#Crawling 이 끝나면 mysql 데이터베이스로 들어가서 "UPDATE cr_jobs_internships SET status = 'E' WHERE status = 'P'" 를 해준다. 그러면 크롤링에 실패한 항목들의 status
#를 'E' 로 바꿀수 있다. 

#import scray, MySQLdb, urllib, and re
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from categories.items import CategoriesItem
from ConfigParser import *
import MySQLdb
import urllib
import re

#Define Global variables 
SPIDER_NAME = "internships2"
DESCRIPTION_TMPL = '<div class="section description" itemprop="description">(.*?)<div class="section apply apply-bottom clearfix">'
SITE_URL = "https://www.internships.com"
DOMAIN = "internships.com"

#XPath
TITLE_XPATH = '//div[@class="internship-detail-header"]/h1/text()'
COMPANY_NAME_XPATH = '//div[@class="company-name"]/span/text()'
APPLICATION_DEADLINE_XPATH = '//div[@class="section i-info"]/div[2]/span/text()'
ADDRESS_XPATH = '//div[@class="location"]/div[2]/text()'
POSITION_XPATH = '//div[@class="section i-info"]/div[3]/span/text()'


#JOB DESCRIPTION 페이지에서 HTML DATA 를 가져온다.
def extract_html(url):
	data = urllib.urlopen(url)
	page = data.read()

	#DESCRIPTION_TMPL 에 따라 parse 한다. 
	section_matcher = re.compile(DESCRIPTION_TMPL, re.DOTALL)
	section_list = section_matcher.findall(page)

	#List 를 return 하기 때문에 string 으로 바꿔준다. 
	html_dat = ""
	for item in section_list:
		html_dat = html_dat + item.strip()
	return html_dat

#START URL들은 크롤링 하면서 필요한 정보를 가져온다. 
class MySpider(BaseSpider):
	name = SPIDER_NAME	
	allowed_domains = [DOMAIN]
	db = MySQLdb.connect(host = "221.143.46.115",user = "askstoryteam",passwd = "qlwmsoqkfths",db = "askstoryci_test")
	cursor = db.cursor()

	# 아직 PROCESS 가 되지 않은 URL 들을 가지고 와서 2차 정보를 수집한다. Status 가 'P' 가 아니라면 크롤링을 하지 않는다. 
	sql = "SELECT url FROM cr_jobs_internships WHERE status = 'P';"
	cursor.execute(sql)

	incomplete_urls = list(cursor.fetchall())
	incomplete_urls = list(set(incomplete_urls))
	complete_urls = []

	#데이터 베이스의 url 을 https 형식에 맞게 바꿔준다.
	for url in incomplete_urls:
		url  = str(url)
		length = len(url)
		url = url[2:length-3]
		complete_url = SITE_URL + url
		complete_urls.append(complete_url)
	start_urls = complete_urls

	#START_URLS 에 있는 URL 들을 크롤링 하면서 필요한 2차 정보를 수집한다(xpath 를 통하여 필요한 정보를 가져온다). 수집된 정보는 pipelines.py 에 따라 mysql database 에 저장된다. 
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		job = CategoriesItem()

		job["title"] = hxs.select(TITLE_XPATH).extract()
		job["company_name"] = hxs.select(COMPANY_NAME_XPATH).extract()

		#address 가 virtual 일때를 고려하여야 한다. 
		addr = hxs.select(ADDRESS_XPATH).extract()
		if len(addr) == 0:
			job["address"] = "Virtual"
		else:
			job["address"] = addr

		job["application_deadline"] = hxs.select(APPLICATION_DEADLINE_XPATH).extract()

		#position 이 없을때를 고려하여야 한다. 
		position = hxs.select(POSITION_XPATH).extract()
		if len(position) == 0:
			job["position"] = "Not Provided"
		else:
			job["position"] = position

		#mysql 데이터 베이스에 저장되어있는 url 형식에 맞게 바꿔준다.  
		url = response.url
		start = url.find("www.internships.com")
		job["current_url"] = url[start + 19:]

		#위에 define 된 extract_html 함수를 이용하여서 html 데이터를 가져온다. 
		job["html_dat"] = extract_html(url)

		#job 을 return 하게되면 pipelines.py에 따라 mysql 데이터베이스에 저장된다. 
		return job
