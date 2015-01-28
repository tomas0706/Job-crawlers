# -*- coding: utf-8 -*-
# 이 스파이더를 실행하려면 Terminal 에서 이 파일이 있는 디렉토리로 가서 "scrapy crawl dice2" 라는 명령어를 입력한다. 그러면 스파이더가 자동으로 데이터 크롤링을 시작할 것이다. 크롤링 된 데이터는
# pipelines.py 파일의 명령어에 따라서 mysql 데이터 베이스에 저장 될 것이다. 
# 이 스파이더를 실행하려면 scrapy 를 python 에 설치하여야 한다. (http://scrapy.org/)

# 작성일자: 2014.07.16
# 작성자: 김민


#크롤링이 끝난 후에 mysql 에 들어가서 "UPDATE cr_jobs_dice SET status = 'E' WHERE status = 'P' " 를 해서 크롤링에 실패한 항목들은 E 로 표시해준다. 

#import scrapy, MySQLdb, urllib, and re
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from dice_2nd.items import Dice2NdItem
from ConfigParser import *
import MySQLdb
import urllib
import urllib2
import re

#Global variables
SECTION_TMPL = '<div id="detailDescription">(.*?)</div>'
SPIDER_NAME = "dice2"	
DOMAIN = "dice.com"

#JOB DESCRIPTION 페이지에서 HTML DATA 를 가져온다.
def get_html(url):
	data = urllib.urlopen(url)
	page = data.read()
	section_matcher = re.compile(SECTION_TMPL, re.DOTALL)
	job_description = section_matcher.findall(page)
	#job_description 이 list 이기 때문에 string 으로 바꿔준다.
	html_dat = ""
	for item in job_description:
		html_dat = html_dat + item.strip()

	return html_dat


#START URL들은 크롤링 하면서 필요한 정보를 가져온다. 
class MySpider(BaseSpider):
	name = SPIDER_NAME
	allowed_domains = [DOMAIN]
	db = MySQLdb.connect(host="221.143.46.115",user="askstoryteam",passwd="qlwmsoqkfths",db="askstoryci_test")
	cursor = db.cursor()

	# 아직 PROCESS 가 되지 않은 URL 들을 가지고 와서 2차 정보를 수집한다. Status 가 'P' 가 아니라면 크롤링을 하지 않는다. 
	sql = "SELECT url FROM cr_jobs_dice WHERE status = 'P';"
	cursor.execute(sql)

	incomplete_urls = list(cursor.fetchall())
	#To remove duplicate urls
	incomplete_urls = list(set(incomplete_urls))
	
	complete_urls = []
	#데이터 베이스의 url 을 https 형식에 맞게 바꿔준다.
	for url in incomplete_urls:
		url  = str(url)
		length = len(url)
		url = url[2:length-3]
		url = "http://www.dice.com" + url
		complete_urls.append(url)
	start_urls = complete_urls

	#START_URLS 에 있는 URL 들을 크롤링 하면서 필요한 2차 정보를 수집한다. 수집된 정보는 pipelines.py 에 따라 mysql database 에 저장된다. 
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		job = Dice2NdItem()
		url = response.url
		original_url = response.request.url

		start = original_url.find("www.dice.com")
		job["current_url"] = original_url[start + 12:]
		job["html_dat"] = get_html(url)
		
		return job