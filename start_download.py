#!/usr/bin/env python
# -*- coding:utf-8 -*-
import asyncio
import os
import time
from threading import Thread

__author__ = 'aniss'
import redis


def redis_push(pool, name, url):
    r = redis.Redis(connection_pool=pool)
    r.lpush("apks", name + "," + url)


def get_redis():
    connection_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True)
    return redis.Redis(connection_pool=connection_pool)


def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


async def async_download(name, url):

    print('Start wget %s...' % name)

    dir = "download_apks/" + name.split(".")[1][0]
    try:
        if not os.path.isdir(dir):
            os.mkdir(dir)
        command = 'proxychains wget "%s" -O %s/%s.pkg' % (url, dir, name)

        dl = await asyncio.create_subprocess_shell(command)
        # await download(name, url)
        await dl.wait()
        print('Complete wget %s...' % name)
    except Exception as e:
        print(e)



if __name__ == '__main__':
    # pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
    # redis_push(pool, name="com.qq.exe",
    #            url='https://sm.myapp.com/original/Audio/QQMusic_Setup_1598.4685_QMgr-15.9.5.0.exe')
    # redis_push(pool, name="com.qmusic.exe", url='https://sm.myapp.com/original/im/QQ9.0.3-9.0.3.23743.exe')
    # r = redis.Redis(connection_pool=pool)
    # r.lrange("apks", 0, -1)
    # main()

    # print(r.rpop("apks"))
    if not os.path.isdir("download_apks"):
        os.mkdir("download_apks")
    rcon = get_redis()
    new_loop = asyncio.new_event_loop()
    t = Thread(target=start_loop, args=(new_loop,))
    t.setDaemon(True)
    t.start()

    try:
        while True:
            value = rcon.rpop("apks")

            if not value:
                time.sleep(1)
                print('.', end="")
                continue
            name, url = value.split(",")
            asyncio.run_coroutine_threadsafe(async_download(name, url), new_loop)
    except Exception as e:
        print(e)
        new_loop.stop()
    finally:
        pass