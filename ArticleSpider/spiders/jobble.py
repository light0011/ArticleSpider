# -*- coding: utf-8 -*-
import scrapy


class JobbleSpider(scrapy.Spider):
    name = 'jobble'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/111551/']

    def parse(self, response):
        select_list = response.xpath('//*[@id="post-111551"]/div[1]/h1')
        print(select_list)
        pass
