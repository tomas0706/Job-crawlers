
# -*- coding: utf-8 -*-
import sys; sys.path.append("/opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages")
import MySQLdb
import hashlib
from scrapy.exceptions import DropItem
from scrapy.http import Request

#스파이더로 수집한 데이터를 mysql 데이터베이스 askstoryci_test.cr_jobs_internships 테이블에 저장한다. Company_name, title, address,html_dat, application_deadline, position 등을 저장한다. 
class Snagajob2NdPipeline(object):
	def __init__(self):
		self.conn = MySQLdb.connect(host="221.143.46.115",user="askstoryteam",passwd="qlwmsoqkfths",db="askstoryci_test", charset='utf8', use_unicode=True)
		self.cursor = self.conn.cursor()
		self.conn.commit()
	def process_item(self, item, spider):
		try:
			self.cursor.execute("""UPDATE cr_jobs_snagajob SET html_dat = %s, status = "R" WHERE url = %s""", (item['html_dat'], item['current_url']))
		except MySQLdb.Error, e:
			print "Error %d: %s" % (e.args[0], e.args[1])
		return item




