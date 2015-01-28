# -*- coding: utf-8 -*-
import sys; sys.path.append("/opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages")
import MySQLdb
import hashlib
from scrapy.exceptions import DropItem
from scrapy.http import Request

class Snag1StPipeline(object):
     def __init__(self):
         self.conn = MySQLdb.connect(host="221.143.46.115",user="askstoryteam",passwd="qlwmsoqkfths",db="askstoryci_test")
         self.cursor = self.conn.cursor()

     def process_item(self, item, spider):
         try:
             self.cursor.execute("""INSERT INTO cr_jobs_snagajob (url, category, local, region, company_name, title) VALUES (%s, %s, %s, %s, %s, %s)""", (item['url'], item['category'], item['local'], item['region'], item['company_name'], item['title']))
             self.conn.commit()
         except MySQLdb.Error, e:
             print "Error %d: %s" % (e.args[0], e.args[1])

         return item
