# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from  scrapy.exporters import JsonLinesItemExporter
import MySQLdb


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item



#下载图片，并且将下载后的本地图片路径放入item中
class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        # if isinstance(item, dict) or self.images_result_field in item.fields:
        item['local_img_url'] = [x['path'] for ok, x in results if ok]
        return item

#将数据保存为json格式
class ArticleJsonSavePipeline(object):
    def __init__(self):
        self.file = open('data.json', 'wb')
        self.exporter = JsonLinesItemExporter(self.file)
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


#将数据存入到mysql中
class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('172.16.98.12', 'xin', '48sdf37EB7', 'xin', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into scrapy(title, remote_img_url, local_img_url, publish_date,praise_nums,fav_nums,comment_nums,tags,content)
            VALUES ('%s', '%s', '%s', '%s',%s, %s, %s, '%s','%s')
        """

        insert_sql = insert_sql %(item["title"], item["remote_img_url"][0], item["local_img_url"][0], item["publish_date"], item["praise_nums"],item["fav_nums"], item["comment_nums"], item["tags"],item['content'])

        self.cursor.execute(insert_sql)
        self.conn.commit()
        return item