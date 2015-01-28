# -*- coding: utf-8 -*-

# Scrapy settings for snag_1st project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'snag_1st'

SPIDER_MODULES = ['snag_1st.spiders']
NEWSPIDER_MODULE = 'snag_1st.spiders'

ITEM_PIPELINES = [
	'snag_1st.pipelines.Snag1StPipeline',
]

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'snag_1st (+http://www.yourdomain.com)'
