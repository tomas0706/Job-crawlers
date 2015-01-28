# -*- coding: utf-8 -*-
import sys; sys.path.append("/opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages")
import MySQLdb
import hashlib
from scrapy.exceptions import DropItem
from scrapy.http import Request

class Dice1StPipeline(object):
     def __init__(self):
         self.conn = MySQLdb.connect(host="221.143.46.115",user="askstoryteam",passwd= ,db="askstoryci_test")
         self.cursor = self.conn.cursor()

     def process_item(self, item, spider):
         try:
             self.cursor.execute("""INSERT INTO cr_jobs_dice (skill, url, title, company_name, address, posted_date) VALUES (%s, %s, %s, %s, %s, %s)""", (item['skill'], item['url'], item['title'], item['company_name'], item['address'], item['posted_date']))
             self.conn.commit()
         except MySQLdb.Error, e:
             print "Error %d: %s" % (e.args[0], e.args[1])

         return item

