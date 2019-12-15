# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZufangSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 房屋ID
    room_id = scrapy.Field()
    # 房间ID
    house_id = scrapy.Field()
    # 城市编号
    city_code = scrapy.Field()
    # 房屋URL
    url = scrapy.Field()
    # 房屋编号
    zoom_no = scrapy.Field()
    # 房屋标题
    title = scrapy.Field()
    # 房屋状态
    status = scrapy.Field()
    # 房屋描述
    desc = scrapy.Field()
    # 房屋图片
    imgs = scrapy.Field()
    # 房屋图片路径
    imgs_path = scrapy.Field()
    # 价格_图片
    price_url = scrapy.Field()
    # 价格_图片路径
    price_url_path = scrapy.Field()

    # 价格_月付
    price_m = scrapy.Field()
    # 价格_月付_原价
    price_m_pre = scrapy.Field()
    # 服务费/年_月付
    price_ms = scrapy.Field()
    # 服务费/年_月付_原价
    price_ms_pre = scrapy.Field()
    # 押金_月付
    price_md = scrapy.Field()
    # 押金_月付_原价
    price_md_pre = scrapy.Field()

    # 价格_季付
    price_q = scrapy.Field()
    # 价格_季付_原价
    price_q_pre = scrapy.Field()
    # 服务费/年_季付
    price_qs = scrapy.Field()
    # 服务费/年_季付_原价
    price_qs_pre = scrapy.Field()
    # 押金_季付
    price_qd = scrapy.Field()
    # 押金_季付_原价
    price_qd_pre = scrapy.Field()

    # 价格_半年付
    price_h = scrapy.Field()
    # 价格_半年付_原价
    price_h_pre = scrapy.Field()
    # 服务费/年_半年付
    price_hs = scrapy.Field()
    # 服务费/年_半年付_原价
    price_hs_pre = scrapy.Field()
    # 押金_半年付
    price_hd = scrapy.Field()
    # 押金_半年付_原价
    price_hd_pre = scrapy.Field()

    # 价格_年付
    price_y = scrapy.Field()
    # 价格_年付_原价
    price_y_pre = scrapy.Field()
    # 服务费/年_年付
    price_ys = scrapy.Field()
    # 服务费/年_年付_原价
    price_ys_pre = scrapy.Field()
    # 押金_年付
    price_yd = scrapy.Field()
    # 押金_年付_原价
    price_yd_pre = scrapy.Field()

    # 价格_自如客
    price_z = scrapy.Field()
    # 价格_自如客_原价
    price_z_pre = scrapy.Field()
    # 服务费/年_自如客
    price_zs = scrapy.Field()
    # 服务费/年_自如客_原价
    price_zs_pre = scrapy.Field()
    # 押金_自如客
    price_zd = scrapy.Field()
    # 押金_自如客_原价
    price_zd_pre = scrapy.Field()

    # 优惠
    tip = scrapy.Field()
    # 信用免押
    credit_plan = scrapy.Field()
    # 海燕计划
    plan1 = scrapy.Field()
    # 惠蕾计划
    plan2 = scrapy.Field()
    # 入住礼包
    gift_plan = scrapy.Field()
    # 房屋设备
    labels = scrapy.Field()
    # 房屋标签
    tags = scrapy.Field()
    # tags2 = scrapy.Field()
    # tags3 = scrapy.Field()
    # tags4 = scrapy.Field()
    # tags5 = scrapy.Field()
    # tags6 = scrapy.Field()
    # 建筑面积
    area_room = scrapy.Field()
    # 朝向
    towards = scrapy.Field()
    # 户型
    type_room = scrapy.Field()
    # 位置
    address = scrapy.Field()
    # 楼层
    floors = scrapy.Field()
    # 房子年代
    ftime = scrapy.Field()
    # 是否配备电梯
    elevator = scrapy.Field()
    # 供暖
    heating = scrapy.Field()
    # 绿化
    green = scrapy.Field()
    # 空置时长
    air_time = scrapy.Field()
    # 检测日期
    air_date = scrapy.Field()
    # 检测报告
    air_url = scrapy.Field()
    # 入住日期
    info_time = scrapy.Field()
    # 签约时长
    info_length = scrapy.Field()
    # 签约注意事项
    info_url = scrapy.Field()
    # 整租OR合租
    house_type = scrapy.Field()

    # 小区信息
    # 名称
    jname = scrapy.Field()
    # 建筑年代
    jtime = scrapy.Field()
    # 建筑类型
    jtype = scrapy.Field()
    # 供暖方式
    jheating = scrapy.Field()
    # 绿化率
    jgreen = scrapy.Field()
    # 容积率
    plot_ratio = scrapy.Field()
    # 物业公司
    property = scrapy.Field()
    # 物业电话
    property_ph = scrapy.Field()









