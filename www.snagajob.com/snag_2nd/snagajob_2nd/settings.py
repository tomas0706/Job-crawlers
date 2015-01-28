# -*- coding: utf-8 -*-

# Scrapy settings for snagajob_2nd project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'snagajob_2nd'

SPIDER_MODULES = ['snagajob_2nd.spiders']
NEWSPIDER_MODULE = 'snagajob_2nd.spiders'

REDIRECT_ENABLED = False

ITEM_PIPELINES = [
	'snagajob_2nd.pipelines.Snagajob2NdPipeline',
]

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'snagajob_2nd (+http://www.yourdomain.com)'
