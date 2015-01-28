# -*- coding: utf-8 -*-

# Scrapy settings for internships project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'internships'

SPIDER_MODULES = ['internships.spiders']
NEWSPIDER_MODULE = 'internships.spiders'

ITEM_PIPELINES = [
	'internships.pipelines.InternshipsPipeline',
]

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'internships (+http://www.yourdomain.com)'
