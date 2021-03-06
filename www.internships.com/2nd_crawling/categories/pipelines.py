# -*- coding: utf-8 -*-
import sys; sys.path.append("/opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages")
import MySQLdb
import hashlib
from scrapy.exceptions import DropItem
from scrapy.http import Request

#스파이더로 수집한 데이터를 mysql 데이터베이스 askstoryci_test.cr_jobs_internships 테이블에 저장한다. Company_name, title, address,html_dat, application_deadline, position 등을 저장한다. 
class CategoriesPipeline(object):
	def __init__(self):
		self.conn = MySQLdb.connect(host="221.143.46.115",user="askstoryteam",passwd="",db="askstoryci_test", charset='utf8', use_unicode=True)
		self.cursor = self.conn.cursor()
		self.conn.commit()
	def process_item(self, item, spider):
		try:
			self.cursor.execute("""UPDATE cr_jobs_internships SET company_name = %s, title = %s, address = %s, html_dat = %s, application_deadline = %s, position = %s, status = "R" WHERE url = %s""", (item['company_name'], item['title'], item['address'],item['html_dat'], item['application_deadline'], item['position'], item['current_url']))
		except MySQLdb.Error, e:
			print "Error %d: %s" % (e.args[0], e.args[1])
		return item




