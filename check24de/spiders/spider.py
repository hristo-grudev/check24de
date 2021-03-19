import scrapy

from scrapy.loader import ItemLoader

from ..items import Check24deItem
from itemloaders.processors import TakeFirst


class Check24deSpider(scrapy.Spider):
	name = 'check24de'
	start_urls = ['https://www.check24.de/unternehmen/presse/pressemitteilungen/?year=&year=&month=0&category=C24+Bank&searchterm']

	def parse(self, response):
		post_links = response.xpath('//a[@class="c24-pressreleases-box"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//em//text()[normalize-space()] | //*[contains(concat( " ", @class, " " ), concat( " ", "c24-pressrelease-text", " " ))]//text()[normalize-space()] | //*[(@id = "c24-container-2")]//strong//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//span[@class="c24-pressrelease-head"]/text()').get().split('|')[0]

		item = ItemLoader(item=Check24deItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
