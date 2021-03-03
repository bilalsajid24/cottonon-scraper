BOT_NAME = 'cottonon_crawler'

SPIDER_MODULES = ['cottonon_crawler.spiders']
NEWSPIDER_MODULE = 'cottonon_crawler.spiders'

DOWNLOAD_DELAY = 0

ROBOTSTXT_OBEY = False
COOKIES_DEBUG = False
LOG_LEVEL = 'DEBUG'

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
