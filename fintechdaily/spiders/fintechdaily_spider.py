import scrapy
from fintechdaily.items import FintechdailyItem
from scrapy.selector import Selector
import json

class FintechdailySpider(scrapy.Spider):
    name = "fintechdaily"

    def start_requests(self):
        urls = [
            # q=fintech日报
            'http://search.cebnet.com.cn/getjsonp?q=fintech%E6%97%A5%E6%8A%A5&p=1'
        ]
        #allowed_domains = ["cebnet.com.cn"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item = FintechdailyItem()
        resp_data = response.body_as_unicode().strip("jsonpCallback(").strip(")")
        resp_json = json.loads(resp_data)[1]
        item['origin_url'] = "http:" + resp_json['url'].strip()
        item['post_time'] = resp_json['date'].strip()
        item['title'] = resp_json['desc'].strip()
        item['media_source'] = resp_json['media'].strip()
        item['post_url'] = ''

        yield scrapy.Request(url=item['origin_url'], meta={'item': item}, callback=self.parse_post)

    def parse_post(self, response):
        item = response.meta['item']
        selector = Selector(response)
        image_url = "http:" + selector.xpath('/html/body/div[4]/div[1]/div[3]/div[1]/p[1]/img/@src').extract()[0]
        item['origin_url'] = image_url
        return item