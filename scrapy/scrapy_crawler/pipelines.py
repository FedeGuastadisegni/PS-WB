# -*- coding: utf-8 -*-
import re
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals


class ScrapRapiPagoPipeline(object):

    def process_item(self, item, spider):
        item['address'] = self.cleanup_address(item['address'])
        item.save()
        return item

    def cleanup_address(self, address):
        m = re.search('(?P<numb>(\d+))\s(?P=numb)', address)
        if m:
            return address[0:m.end(1)]
        return address

    def __init__(self, stats, settings):
    	self.stats = stats
    	dispatcher.connect(self.save_crawl_stats,signals.spider_closed)

	@classmethod
	def from_crawler(cls, crawler):
    	return cls(crawler.stats,crawler.settings)

	def save_crawl_stats(self):
    	record_crawl_stats(self.cur,self.stats,self.crawl_instance)