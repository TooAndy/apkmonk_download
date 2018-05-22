# -*- coding: utf-8 -*-
import telnetlib
import os

import time


def get_wget_pros_num():
    command = "ps aux | grep '/bin/sh -c wget' | grep -v grep | wc"
    num = os.popen(command, 'r', 1).read().strip().split(" ")[0]
    num = int(num)
    return num


def is_spider_alive(spider=""):
    if spider == "":
        # use this when you start scrapy with start_scrapy.py
        comand = "ps aux | grep 'start_scrapy.py' | grep -v grep | wc"
    else:
        # use this when you start scrapy with CLI
        comand = "ps aux | grep 'scrapy crawl %s' | grep -v grep | wc" % spider

    status = os.popen(comand).read().strip().split(" ")[0]
    return int(status) >= 1


def main(max, min):
    HOST = "localhost"
    PORT = 6023
    is_pause = False
    if not is_spider_alive("apkmonk"):
        print("\n----Please start scrapy first----\n")
        return
    try:
        tn = telnetlib.Telnet(host=HOST, port=PORT)
        print("create connection successful")
        while is_spider_alive("apkmonk"):
            num = get_wget_pros_num()
            info = ("pausing, num = %s" % num) if is_pause else ("running, num = %s" % num)
            print(info)
            if (not is_pause) and num > max:
                tn.write("engine.pause()\n".encode('ascii'))
                is_pause = True
                print("engine.pause()")

            elif is_pause and num < min:
                tn.write("engine.unpause()\n".encode('ascii'))
                is_pause = False
                print("engine.unpause()")

            time.sleep(1)
    except Exception as e:
        print(e, "\n\n----Please start scrapy first----\n")


if __name__ == '__main__':
    main(20, 5)
