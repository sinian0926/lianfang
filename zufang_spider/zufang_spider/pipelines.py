# -*- coding: utf-8 -*-
import os
from scrapy.http import Request
from scrapy.pipelines.images import ImagesPipeline
import shutil


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class ZufangSpiderPipeline(object):
    def process_item(self, item, spider):
        return item


# 自定义图片下载pipeline
class ZiroomImagesPipeline(ImagesPipeline):

    def item_completed(self, results, item, info):
        zoom_no = item["zoom_no"]
        for ok, value in results:
            project_dir = os.path.abspath(os.path.dirname(__file__)) + "/ziroom_imgs/"
            imgs_dir_path = os.path.join(project_dir, zoom_no)
            if not os.path.exists(imgs_dir_path):
                os.mkdir(imgs_dir_path)
            if value["path"].find(".png") != -1:
                os.rename(project_dir + value["path"], imgs_dir_path + "/" + zoom_no + "_price.png")
                item["price_url_path"] = imgs_dir_path + "/" + zoom_no + "_price.png"
            else:
                item["imgs_path"] = shutil.move(project_dir + value["path"], imgs_dir_path)
        return item
