# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import urllib.request
import time
import fintechdaily.settings as settings
import pymysql

class FintechdailyPipeline(object):
    def process_item(self, item, spider):
        file_date = time.strftime('%Y%m%d', time.localtime(time.time()))
        file_name = file_date + item['origin_url'].split('/')[-1]
        urllib.request.urlretrieve(item['origin_url'], settings.POST_STORE + '/' + file_name)
        item['post_url'] = settings.POST_HOST + '/' + settings.POST_PATH + '/' + file_name
        self.insert_item(item)
        return item

    def insert_item(self, item):
        db = pymysql.connect(host=settings.DATABASE_HOST, user=settings.DATABASE_USER, password=settings.DATABASE_PASS,\
                             db=settings.DATABASE_NAME, charset=settings.DATABASE_CHARSET, port=settings.DATABASE_PORT)
        cursor = db.cursor()
        sql = "INSERT INTO fintech_daily(title, media_source, post_time, origin_url, post_url) \
                VALUES ('%s', '%s','%s', '%s', '%s')" % \
              (item['title'], item['media_source'], item['post_time'], item['origin_url'], item['post_url'])
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
        db.close()