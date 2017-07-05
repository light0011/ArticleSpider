# -*- coding: utf-8 -*-
import scrapy
import re
import json
import datetime
import random
from ArticleSpider.settings import USER_AGENT_LIST

class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    random_index = random.randint(0,len(USER_AGENT_LIST)-1)

    # random_agent = USER_AGENT_LIST[random_index]
    headers = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhizhu.com",
        # 'User-Agent': random_agent,
    }

    def parse(self, response):
        pass

    def start_requests(self):
        return [scrapy.Request('https://www.zhihu.com/#signin', headers=self.headers,callback=self.login)]

    def login(self, response):
        response_text = response.text
        match_obj = re.match('.*name="_xsrf" value="(.*?)"',response_text,re.DOTALL)
        xrsf = ''

        if match_obj:
            xrsf = match_obj.group(1)

        if xrsf:
            post_url = "https://www.zhihu.com/login/phone_num"
            post_data = {
                "_xsrf":  xrsf,
                "phone_num": "17600118856",
                "password": "qqqpppqqqppp",
                "captcha": ""
            }

            import time
            t = str(int(time.time() * 1000))
            captcha_url = "https://www.zhihu.com/captcha.gif?r={0}&type=login".format(t)
            yield scrapy.Request(captcha_url, headers=self.headers, meta={"post_data": post_data},
                                 callback=self.login_after_captcha)

    def login_after_captcha(self, response):
        with open("captcha.jpg", "wb") as f:
            f.write(response.body)
            f.close()

        from PIL import Image
        try:
            im = Image.open('captcha.jpg')
            im.show()
            im.close()
        except:
            pass

        captcha = input("输入验证码\n>")

        post_data = response.meta.get("post_data", {})
        post_url = "https://www.zhihu.com/login/phone_num"
        post_data["captcha"] = captcha
        return [scrapy.FormRequest(
            url=post_url,
            formdata=post_data,
            headers=self.headers,
            callback=self.check_login
        )]

    def check_login(self, response):
        #验证服务器的返回数据判断是否成功
        text_json = json.loads(response.text)
        if "msg" in text_json and text_json["msg"] == "登录成功":
            for url in self.start_urls:
                yield scrapy.Request(url, dont_filter=True, headers=self.headers)
