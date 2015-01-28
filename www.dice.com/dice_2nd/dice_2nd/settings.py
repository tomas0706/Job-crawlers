# -*- coding: utf-8 -*-

# Scrapy settings for dice_2nd project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'dice_2nd'

SPIDER_MODULES = ['dice_2nd.spiders']
NEWSPIDER_MODULE = 'dice_2nd.spiders'

REDIRECT_ENABLED = False

ITEM_PIPELINES = [
	'dice_2nd.pipelines.Dice2NdPipeline',
]

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'dice_2nd (+http://www.yourdomain.com)'
