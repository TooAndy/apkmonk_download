#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'aniss'

import os
import asyncio
import logging
import time


# def download(name, url):
#     dir = name.split(".")[1][0]
#     command = 'proxychains wget "%s" -O %s/%s.pkg' % (url, dir, name)
#     os.system(command)


async def async_download(name, url):
    logger = logging.Logger(__name__)
    logger.info('Start wget %s...' % name)

    dir = name.split(".")[1][0]
    if not os.path.isdir(dir):
        os.mkdir(dir)
    command = 'proxychains wget "%s" -O %s/%s.pkg > /dev/null' % (url, dir, name)

    dl = await asyncio.create_subprocess_shell(command)
    # await download(name, url)
    await dl.wait()
    logger.info('Complete wget %s...' % name)


if __name__ == '__main__':
    # pass
    loop = asyncio.get_event_loop()
    # loop.create_task()
    tasks = [async_download("com.qq.exe", 'https://sm.myapp.com/original/im/QQ9.0.3-9.0.3.23743.exe'),
             async_download("com.qmusic.exe",
                            "https://sm.myapp.com/original/Audio/QQMusic_Setup_1598.4685_QMgr-15.9.5.0.exe")]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()


# import asyncio
#
#
# @asyncio.coroutine
# def wget(host):
#     print('wget %s...' % host)
#     connect = asyncio.open_connection(host, 80)
#     reader, writer = yield from connect
#     header = 'GET / HTTP/1.0\r\nHost: %s\r\n\r\n' % host
#     writer.write(header.encode('utf-8'))
#     yield from writer.drain()
#     while True:
#         line = yield from reader.readline()
#         if line == b'\r\n':
#             break
#         print('%s header > %s' % (host, line.decode('utf-8').rstrip()))
#     # Ignore the body, close the socket
#     writer.close()
#
#
# loop = asyncio.get_event_loop()
# tasks = [wget(host) for host in ['www.sina.com.cn', 'www.sohu.com', 'www.163.com']]
# loop.run_until_complete(asyncio.wait(tasks))
# loop.close()
