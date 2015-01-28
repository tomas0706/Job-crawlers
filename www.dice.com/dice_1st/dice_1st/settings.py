# -*- coding: utf-8 -*-

# Scrapy settings for dice_1st project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'dice_1st'

SPIDER_MODULES = ['dice_1st.spiders']
NEWSPIDER_MODULE = 'dice_1st.spiders'


ITEM_PIPELINES = [
	'dice_1st.pipelines.Dice1StPipeline',
]

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'dice_1st (+http://www.yourdomain.com)'
