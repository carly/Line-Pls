import scrapy

from backstage.items import BackstageItem
from scrapy.selector import Selector


class BackstageSpider(scrapy.Spider):
	name = "backstage"
	allowed_domains = ["www.backstage.com"]
	start_urls = [
		"http://www.backstage.com/monologues/"
	]

	def parse(self, response):
		for sel in response.xpath('//div[@id="main"]'):
			item = BackstageItem()
			item['title'] = sel.xpath('//div[@class="monologue-title"]/h3/text()').extract()
			item['author'] = sel.xpath('//div[@class="monologue-author"]/h4/text()').extract()
			item['scene_synopsis'] = sel.xpath('//div[@id="scene-synopsis"]/div[@class="panel-body"]/text()').extract()
			item['play_synopsis'] = sel.xpath('//div[@id="play-synopsis"]/div[@class="panel-body"]/text()').extract()
			item['monologue_text'] = sel.xpath('//div[@class="monologue-text"]').extract()
			yield item 