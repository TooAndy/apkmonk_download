# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.files import FilesPipeline
from scrapy.pipelines.images import ImagesPipeline


class ApksPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = open('image1.json', 'w+')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        self.file.flush()
        return item


class CustomPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):  # 重写ImagesPipeline   get_media_requests方法
        '''
        :param item:
        :param info:
        :return:
        在工作流程中可以看到，
        管道会得到文件的URL并从项目中下载。
        为了这么做，你需要重写 get_media_requests() 方法，
        并对各个图片URL返回一个Request:
        '''
        # headers = {
        #     "Referer": item['image_urls']
        # }
        # logger = logging.Logger(__name__)
        # logger.info("Use proxy:127.0.0.1:8081")
        meta = {'group_id': item['group_id'],
                "proxy": "10.104.4.68:1081"
                }

        yield scrapy.Request(item['app_front_img_url'], meta=meta)

    def file_path(self, request, response=None, info=None):
        name = request.meta["group_id"]
        dir = name.split(".")[1][0]
        if (dir.isupper()):
            dir = dir.lower() * 2
        path = '%s/%s.jpg' % (dir, name)
        return path

    def item_completed(self, results, item, info):
        '''
        :param results:
        :param item:
        :param info:
        :return:
        当一个单独项目中的所有图片请求完成时（要么完成下载，要么因为某种原因下载失败），
         item_completed() 方法将被调用。
        '''
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no files")
        return item
