#!/usr/bin/env python
# -*- coding: utf-8 -*-
import redis

__author__ = 'aniss'
from scrapy.cmdline import execute
import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))


def name(name):
    res = ''.join(name.split('_')[-2:]).strip('/')
    print(res)





if __name__ == '__main__':
    execute("scrapy crawl google".split(" "))
    # redis_push("com.axlebolt.standoff2", 'https://www.apkmonk.com/download-app/com.sanandreas.autotheft')

    # value = 'https://www.apkmonk.com/download-app/com.sanandreas.autotheft.' \
    #        'gat.freegames/5_com.sanandreas.autotheft.gat.freegames_2018-05-14.apk/'
    # name(value)
    # pkg, key = "/download-app/com.axlebolt.standoff2/4_com.axlebolt.standoff2_2018-05-12.apk/".split("/")[-3:-1]
    # url = "/down_file/?pkg={0}&key={1}".format(pkg, key)
    # print(url)
    # name = "com"
    # print(name[0])
