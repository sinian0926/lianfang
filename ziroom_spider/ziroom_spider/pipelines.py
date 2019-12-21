# -*- coding: utf-8 -*-
import os
from scrapy.pipelines.images import ImagesPipeline
import shutil
import json
import pymysql.cursors
import pymysql
from twisted.enterprise import adbapi


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class ZufangSpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class ZufangMySQLPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbpram = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DB"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWD"],
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool("pymysql", **dbpram)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 异步插入数据库
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error)

    def handle_error(self, failure):
        print(failure)

    def do_insert(self, cursor, item):
        print(item)
        ins_sql = '''
        insert into ziroom_full(room_id,house_id,city_code,url,zoom_no,title,fstatus,fdesc,imgs,imgs_path,price_url,price_m,price_m_pre,price_ms,price_ms_pre,price_md,price_md_pre,price_q,price_q_pre,price_qs,price_qs_pre,price_qd,price_qd_pre,price_h,price_h_pre,price_hs,price_hs_pre,price_hd,price_hd_pre,price_y,price_y_pre,price_ys,price_ys_pre,price_yd,price_yd_pre,price_z,price_z_pre,price_zs,price_zs_pre,price_zd,price_zd_pre,tip,credit_plan,plan1,plan2,gift_plan,labels,tags,area_room,towards,type_room,address,floors,ftime,elevator,heating,green,air_time,air_date,air_url,info_time,info_length,info_url,house_type,jname,jtime,jtype,jheating,jgreen,plot_ratio,property,property_ph)
values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        '''
        cursor.execute(ins_sql, (
            item['room_id'], item['house_id'], item['city_code'], item['url'], item['zoom_no'], item['title'],
            item['status'],
            item['desc'], item['imgs'], item['imgs_path'], item['price_url'], item['price_m'],
            item['price_m_pre'],
            item['price_ms'], item['price_ms_pre'], item['price_md'], item['price_md_pre'], item['price_q'],
            item['price_q_pre'], item['price_qs'],
            item['price_qs_pre'], item['price_qd'], item['price_qd_pre'], item['price_h'], item['price_h_pre'],
            item['price_hs'], item['price_hs_pre'],
            item['price_hd'], item['price_hd_pre'], item['price_y'], item['price_y_pre'], item['price_ys'],
            item['price_ys_pre'], item['price_yd'],
            item['price_yd_pre'], item['price_z'], item['price_z_pre'], item['price_zs'], item['price_zs_pre'],
            item['price_zd'], item['price_zd_pre'],
            item['tip'], item['credit_plan'], item['plan1'], item['plan2'], item['gift_plan'], item['labels'],
            item['tags'],
            item['area_room'], item['towards'],
            item['type_room'], item['address'], item['floors'], item['ftime'], item['elevator'], item['heating'],
            item['green'], item['air_time'], item['air_date'],
            item['air_url'], item['info_time'], item['info_length'], item['info_url'], item['house_type'],
            item['jname'],
            item['jtime'], item['jtype'], item['jheating'],
            item['jgreen'], item['plot_ratio'], item['property'], item['property_ph']))


# 自定义图片下载pipeline
class ZiroomImagesPipeline(ImagesPipeline):

    def item_completed(self, results, item, info):
        zoom_no = item["zoom_no"]
        urls = list()
        imgs = dict()
        for ok, value in results:
            project_dir = os.path.abspath(os.path.dirname(__file__)) + "\\ziroom_imgs\\"
            imgs_dir_path = os.path.join(project_dir, zoom_no)
            if not os.path.exists(imgs_dir_path):
                os.mkdir(imgs_dir_path)

            # 移动图片至房屋编号目录下
            item["imgs_path"] = os.path.abspath(
                os.path.dirname(shutil.move(project_dir + value["path"], imgs_dir_path)))
            # 将房屋图片地址转成JSON格式保存
            urls.append(value["url"])
        imgs["imgs"] = urls
        item["imgs"] = json.dumps(imgs)
        return item
