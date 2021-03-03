import json
import logging
import os

from scrapy import logformatter
from twisted.python.failure import Failure

from .settings import LOG_FORMATTER_ENSURE_ASCII

SCRAPED_MSG = u'Scraped from %(src)s' + os.linesep + '%(item)s'
ITEM_ERROR_MSG = u'Error processing %(item)s'


class JsonFormatter(logformatter.LogFormatter):
    def scraped(self, item, response, spider):
        if isinstance(response, Failure):
            src = response.getErrorMessage()
        else:
            src = response

        return {
            'level': logging.DEBUG,
            'msg': SCRAPED_MSG,
            'args': {
                'src': src,
                'item': json.dumps(dict(item), ensure_ascii=LOG_FORMATTER_ENSURE_ASCII),
            }
        }

    def item_error(self, item, exception, response, spider):
        return {
            'level': logging.ERROR,
            'msg': ITEM_ERROR_MSG,
            'args': {
                'item': json.dumps(dict(item), ensure_ascii=LOG_FORMATTER_ENSURE_ASCII),
            }
        }
