import os

BOT_NAME = 'cottonon_crawler'

SPIDER_MODULES = ['cottonon_crawler.spiders']
NEWSPIDER_MODULE = 'cottonon_crawler.spiders'

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 ' \
             '(KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36'
DOWNLOAD_DELAY = 1

ROBOTSTXT_OBEY = False
COOKIES_DEBUG = False
LOG_LEVEL = os.environ['LOG_LEVEL']

RETRY_HTTP_CODES = [
    '500', '503', '502', '504', '400',
    '408', '404', '403', '413'
]
RETRY_TIMES = 5
RETRY_PRIORITY_ADJUST = 10

LOG_FORMATTER = 'cottonon_crawler.json_formatter.JsonFormatter'
LOG_FORMATTER_ENSURE_ASCII = True

ITEM_PIPELINES = {
   'cottonon_crawler.pipelines.CottononCrawlerPipeline': 300,
}
