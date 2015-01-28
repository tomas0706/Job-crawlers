# -*- coding: utf-8 -*-
import sys; sys.path.append("/opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages")
import MySQLdb
import hashlib
from scrapy.exceptions import DropItem
from scrapy.http import Request


#스파이더가 수집한 데이터를 askstoryci_test 데이터베이스에 있는 cr_jobs_internships로 옮긴다.
class InternshipsPipeline(object):
     def __init__(self):
         self.conn = MySQLdb.connect(host="221.143.46.115",user="askstoryteam",passwd="",db="askstoryci_test")
         self.cursor = self.conn.cursor()

     def process_item(self, item, spider):
         try:
             self.cursor.execute("""INSERT INTO cr_jobs_internships (url, category) VALUES (%s, %s)""", (item['url'], item['category']))
             self.conn.commit()
         except MySQLdb.Error, e:
             print "Error %d: %s" % (e.args[0], e.args[1])

         return item



