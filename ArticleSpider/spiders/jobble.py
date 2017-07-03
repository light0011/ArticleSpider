# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
from ArticleSpider.items import JobboleArticleItem


class JobbleSpider(scrapy.Spider):
    name = 'jobble'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):

        article_list = response.css('#archive .floated-thumb .post-thumb a')
        for article_desc in article_list:
            remote_img_url = article_desc.css('img::attr(src)').extract_first('')
            article_detail_url = article_desc.css('::attr(href)').extract_first('')

            yield Request(url=parse.urljoin(response.url, article_detail_url), meta={'remote_img_url': remote_img_url}, callback=self.parse_detail)

        # 提取到下一页并进行下载
        next_url = response.css('.next::attr(href)').extract_first('')
        if next_url:
            yield Request(url=next_url, callback=self.parse)




    def parse_detail(self, response):
        article_item = JobboleArticleItem()
        
        remote_img_url = response.meta.get('remote_img_url', '')
        title = response.css(".entry-header h1::text").extract()[0]
        publish_date = response.css('.entry-meta-hide-on-mobile::text').extract_first('')[0:-3].strip()
        praise_nums = response.css('.vote-post-up  h10::text').extract_first(0)
        fav_nums = response.css('.bookmark-btn::text').extract_first('').replace('收藏', '').strip()
        fav_nums = fav_nums if fav_nums != '' else 0
        comment_nums = response.css("a[href='#article-comment'] span::text").extract_first('').replace('评论', '').strip()
        comment_nums = comment_nums if comment_nums != '' else 0
        content = response.css('.entry').extract()[0]

        tag_list = response.css('.entry-meta-hide-on-mobile a::text').extract()

        tag_list = [element for element in tag_list if not element.strip().endswith('评论')]

        tags = '-'.join(tag_list)

        article_item['remote_img_url'] = [remote_img_url]
        article_item['title'] = title
        article_item['publish_date'] = publish_date
        article_item['praise_nums'] = praise_nums
        article_item['fav_nums'] = fav_nums
        article_item['comment_nums'] = comment_nums
        article_item['content'] = content
        article_item['tags'] = tags



        yield article_item













