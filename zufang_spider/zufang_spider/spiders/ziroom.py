# -*- coding: utf-8 -*-
import time

import scrapy
import re
from zufang_spider.items import ZufangSpiderItem as ziroom_items

# 图像识别相关
import io
from PIL import Image
import pytesseract
import requests


class ZiroomSpider(scrapy.Spider):
    name = 'ziroom'
    allowed_domains = ['ziroom.com']
    start_urls = ['http://www.ziroom.com/z/p1/']

    def parse(self, response):
        items = ziroom_items()
        info_box = response.xpath("//div[@class='item']/div[@class='info-box']")

        info_url = info_box.xpath("//h5[contains(@class,'sign')]/a/@href").extract()
        info_urls = ['http:' + url for url in info_url]
        # 进入详情页抓取
        for url in ['http:' + url for url in info_url]:
            # 房屋URL
            items["url"] = url

            yield scrapy.Request(url=url, meta={'ul': items}, callback=self.page_parse)
        # # 翻页
        # for x in range(1, 51):
        #     yield scrapy.Request(
        #         url='http://www.ziroom.com/z/p' + str(x) + '/', callback=self.parse)

    def page_parse(self, response):
        # 接收items对象
        items = response.meta['ul']
        # 网页主体
        selector = response.xpath("//section[@class='Z_container Z_main']")
        # 右侧边栏
        right = selector.xpath("./aside[@class='Z_info_aside']")
        # 是否可租
        pre_status = right.xpath("//h1[@class='Z_name']/i/@class").extract_first()
        if pre_status.find("pre") != -1:
            status = "预签"
        else:
            status = "可签"
        items["status"] = status

        # 房屋标题
        title = right.xpath("./h1[@class='Z_name']/text()").extract_first()
        items["title"] = title
        # 整租OR合租
        if title.find("自如寓") != -1:
            house_type = "自如寓"
        elif title.find("整租") != -1:
            house_type = "整租"
        else:
            house_type = "合租"
        items["house_type"] = house_type
        # 信用免押
        credit_plan = right.xpath("./ul[@class='Z_activity']/li[1]/text()").extract()
        items["credit_plan"] = ''.join(credit_plan).strip()
        # 计划1
        plan1 = right.xpath("./ul[@class='Z_activity']/li[2]/text()").extract()
        items["plan1"] = ''.join(plan1).strip()
        # 计划2
        plan2 = right.xpath("./ul[@class='Z_activity']/li[3]/text()").extract()
        items["plan2"] = ''.join(plan2).strip()
        # 入住礼包
        gift_plan = right.xpath("./ul[@class='Z_activity']/li[4]/text()").extract()
        items["gift_plan"] = ''.join(gift_plan).strip()
        # 房屋标签
        tags = right.xpath("./div[@class='Z_tags']//text()").extract()
        # print([str(x).strip() for x in tags1 if ''.__ne__(str(x).strip())])
        items["tags"] = '|'.join([str(x).strip() for x in tags if ''.__ne__(str(x).strip())])
        # 建筑面积
        area_room = right.xpath(
            "./div[@class='Z_home_info']/div[@class='Z_home_b clearfix']/dl[1]/dd/text()").extract_first()
        items["area_room"] = area_room
        # 房屋朝向
        towards = right.xpath(
            "./div[@class='Z_home_info']/div[@class='Z_home_b clearfix']/dl[2]/dd/text()").extract_first()
        items["towards"] = towards
        # 户型
        type_room = right.xpath(
            "./div[@class='Z_home_info']/div[@class='Z_home_b clearfix']/dl[3]/dd/text()").extract_first()
        items["type_room"] = type_room
        # 位置
        address = right.xpath("//span[@class='va']/span[@class='ad']/text()").extract_first()
        items["address"] = address
        # 楼层
        floors = right.xpath(
            "./div[@class='Z_home_info']/ul[@class='Z_home_o']/li[2]/span[@class='va']/text()").extract_first()
        items["floors"] = floors
        # 是否配备电梯
        elevator = right.xpath(
            "./div[@class='Z_home_info']/ul[@class='Z_home_o']/li[3]/span[@class='va']/text()").extract_first()
        items["elevator"] = elevator
        # 房子年代
        ftime = right.xpath(
            "./div[@class='Z_home_info']/ul[@class='Z_home_o']/li[4]/span[@class='va']/text()").extract_first()
        items["ftime"] = ftime
        # 供暖
        heating = right.xpath(
            "./div[@class='Z_home_info']/ul[@class='Z_home_o']/li[5]/span[@class='va']/text()").extract_first()
        items["heating"] = heating
        # 绿化
        green = right.xpath(
            "./div[@class='Z_home_info']/ul[@class='Z_home_o']/li[6]/span[@class='va']/text()").extract_first()
        items["green"] = green

        # 页面主题
        main = selector.xpath("./section[@class='Z_info_main']")
        zoom_no = main.xpath("./div[@id='homedesc']/p[@class='house_sourcecode mt10']/text()").extract_first()
        items["zoom_no"] = str(zoom_no.replace('编号  ', ''))
        # 房屋描述
        desc = main.xpath("./div[@id='homedesc']/div[@class='Z_rent_desc']/text()").extract_first()
        items["desc"] = desc.strip()
        # 房屋设备
        labels = main.xpath("./div[@id='homedesc']/div[@class='Z_info_icons ']/dl//text()").extract()
        items["labels"] = '|'.join([str(x).strip() for x in labels if
                                    ''.__ne__(str(x).strip()) and '更多'.__ne__(str(x).strip()) and '收起'.__ne__(
                                        str(x).strip())])
        # 空置时长
        air_time = main.xpath("./div[@id='areacheck']//li[1]/span[@class='info_value']/text()").extract_first()
        items["air_time"] = air_time
        # 检测日期
        air_date = main.xpath("./div[@id='areacheck']//li[2]/span[@class='info_value']/text()").extract_first()
        items["air_date"] = air_date
        # 检测报告
        air_url = main.xpath("//a[@class='info_value_active text_underline']/@href").extract_first()
        items["air_url"] = air_url
        # 入住日期
        info_time = main.xpath("./div[@id='rentinfo']//li[1]/span[@class='info_value']/text()").extract_first()
        items["info_time"] = info_time.strip()
        # 签约时长
        info_length = main.xpath("./div[@id='rentinfo']//li[2]/span[@class='info_value']/text()").extract_first()
        items["info_length"] = info_length
        # 签约注意事项
        info_url = main.xpath("//a[@class='info_value text_underline']/@href").extract_first()
        items["info_url"] = info_url

        # 小区信息
        community = main.xpath(
            "./div[@id='villageinfo']/div[@class='Z_info_body']//div[@class='Z_village_info']/ul[@class='Z_village_info_body']")
        # 名称
        jname = community.xpath("./h3/text()").extract_first()
        items["jname"] = jname
        # 建筑年代
        jtime = community.xpath("./li[1]/span[@class='value']/text()").extract_first()
        items["jtime"] = jtime
        # 建筑类型
        jtype = community.xpath("./li[2]/span[@class='value']/text()").extract_first()
        items["jtype"] = jtype
        # 供暖方式
        jheating = community.xpath("./li[3]/span[@class='value']/text()").extract_first()
        items["jheating"] = jheating
        # 绿化率
        jgreen = community.xpath("./li[4]/span[@class='value']/text()").extract_first()
        items["jgreen"] = jgreen
        # 容积率
        plot_ratio = community.xpath("./li[5]/span[@class='value']/text()").extract_first()
        items["plot_ratio"] = plot_ratio
        # 物业公司
        property = community.xpath("./li[6]/span[@class='value']/text()").extract_first()
        items["property"] = property
        # 物业电话
        property_ph = community.xpath("./li[7]/span[@class='value']/text()").extract_first()
        items["property_ph"] = property_ph

        # 下载图片和价格处理
        # 房屋图片
        imgs = main.xpath("./div[@id='Z_swiper_box']/div[@class='Z_swiper_thumb']//li/img/@src").extract()
        imgs[0] = imgs[0].replace("https:", "")
        items["imgs"] = ["https:" + img_url for img_url in imgs]

        # 价格
        # 价格_月付
        price_m_style = response.xpath(
            "//div[@id='Z_payWay']/table//tr[1]/td[2]/span[@class='way_num']/@style").extract()
        # 价格_月付偏移
        price_m = [re.findall("background-position: (.*?)px", num)[0] for num in price_m_style]
        # 价格图片地址
        price_url = 'http:' + re.findall(".*\((.*?)\)", price_m_style[0])[0]
        items["price_url"] = price_url
        items["price_m"] = self.parse_price(price_url, price_m)
        # 服务费_月付
        price_ms_style = response.xpath(
            "//div[@id='Z_payWay']/table//tr[1]/td[3]/span[@class='way_num']/@style").extract()
        # 服务费_月付偏移
        price_ms = [re.findall("background-position: (.*?)px", num)[0] for num in price_ms_style]
        items["price_ms"] = self.parse_price(price_url, price_ms)
        # 押金_月付
        price_md_style = response.xpath(
            "//div[@id='Z_payWay']/table//tr[1]/td[4]/span[@class='way_num']/@style").extract()
        # 押金_月付偏移
        price_md = [re.findall("background-position: (.*?)px", num)[0] for num in price_md_style]
        items["price_md"] = self.parse_price(price_url, price_md)
        # 价格_季付
        price_q_style = response.xpath(
            "//div[@id='Z_payWay']/table//tr[2]/td[2]/span[@class='way_num']/@style").extract()
        price_q = [re.findall("background-position: (.*?)px", num)[0] for num in price_q_style]
        items["price_q"] = self.parse_price(price_url, price_q)
        # 服务费_季付
        price_qs_style = response.xpath(
            "//div[@id='Z_payWay']/table//tr[2]/td[3]/span[@class='way_num']/@style").extract()
        price_qs = [re.findall("background-position: (.*?)px", num)[0] for num in price_qs_style]
        items["price_qs"] = self.parse_price(price_url, price_qs)
        # 押金_季付
        price_qd_style = response.xpath(
            "//div[@id='Z_payWay']/table//tr[2]/td[4]/span[@class='way_num']/@style").extract()
        price_qd = [re.findall("background-position: (.*?)px", num)[0] for num in price_qd_style]
        items["price_qd"] = self.parse_price(price_url, price_qd)
        # 价格_半年付
        price_h_style = response.xpath(
            "//div[@id='Z_payWay']/table//tr[3]/td[2]/span[@class='way_num']/@style").extract()
        price_h = [re.findall("background-position: (.*?)px", num)[0] for num in price_h_style]
        items["price_h"] = self.parse_price(price_url, price_h)
        # 服务费_半年付
        price_hs_style = response.xpath(
            "//div[@id='Z_payWay']/table//tr[3]/td[3]/span[@class='way_num']/@style").extract()
        price_hs = [re.findall("background-position: (.*?)px", num)[0] for num in price_hs_style]
        items["price_hs"] = self.parse_price(price_url, price_hs)
        # 押金_半年付
        price_hd_style = response.xpath(
            "//div[@id='Z_payWay']/table//tr[3]/td[4]/span[@class='way_num']/@style").extract()
        price_hd = [re.findall("background-position: (.*?)px", num)[0] for num in price_hd_style]
        items["price_hd"] = self.parse_price(price_url, price_hd)
        # 价格_年付
        price_y_style = response.xpath(
            "//div[@id='Z_payWay']/table//tr[4]/td[2]/span[@class='way_num']/@style").extract()
        price_y = [re.findall("background-position: (.*?)px", num)[0] for num in price_y_style]
        items["price_y"] = self.parse_price(price_url, price_y)
        # 服务费_年付
        price_ys_style = response.xpath(
            "//div[@id='Z_payWay']/table//tr[4]/td[3]/span[@class='way_num']/@style").extract()
        price_ys = [re.findall("background-position: (.*?)px", num)[0] for num in price_ys_style]
        items["price_ys"] = self.parse_price(price_url, price_ys)
        # 押金_年付
        price_yd_style = response.xpath(
            "//div[@id='Z_payWay']/table//tr[4]/td[4]/span[@class='way_num']/@style").extract()
        price_yd = [re.findall("background-position: (.*?)px", num)[0] for num in price_yd_style]
        items["price_yd"] = self.parse_price(price_url, price_yd)
        # 价格_自如客
        price_z_style = response.xpath(
            "//div[@id='Z_payWay']/table//tr[5]/td[2]/span[@class='way_num']/@style").extract()
        price_z = [re.findall("background-position: (.*?)px", num)[0] for num in price_z_style]
        items["price_z"] = self.parse_price(price_url, price_z)
        # 服务费_自如客
        price_zs_style = response.xpath(
            "//div[@id='Z_payWay']/table//tr[5]/td[3]/span[@class='way_num']/@style").extract()
        price_zs = [re.findall("background-position: (.*?)px", num)[0] for num in price_zs_style]
        items["price_zs"] = self.parse_price(price_url, price_zs)
        # 押金_自如客
        price_zd_style = response.xpath(
            "//div[@id='Z_payWay']/table//tr[5]/td[4]/span[@class='way_num']/@style").extract()
        price_zd = [re.findall("background-position: (.*?)px", num)[0] for num in price_zd_style]
        items["price_zd"] = self.parse_price(price_url, price_zd)

        print(items)

        # yield items

    # 识别图片价格
    def parse_price(self, price_url, price_offset):

        if len(price_offset) == 0:
            return 0

        price_list = ["-0", "-18.1", "-36.2", "-54.3", "-72.4", "-90.5", "-108.6", "-126.7", "-144.8", "-162.9"]
        data = requests.get(url=price_url).content
        image = Image.open(io.BytesIO(data))
        vcode = pytesseract.image_to_string(image, lang='eng',
                                            config='--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789').strip()
        ret_list = []
        for i in vcode:
            if ''.__ne__(i.strip()):
                ret_list.append(i)
        # 可能或出现斜杠/或者读取不出
        if '/' in ret_list:
            ret_list.remove('/')
        res = dict(zip(price_list, ret_list))
        price = [res.get(p, "") for p in price_offset]
        return int(''.join(price))

