# -*- coding: utf-8 -*-
import telnetlib
import os

import time


def get_wget_pros_num():
    command = "ps aux | grep wget | grep -v grep | wc"
    num = os.popen(command, 'r', 1).read().strip().split(" ")[0]
    num = int(num)
    return num


def main():
    HOST = "localhost"
    PORT = 6023
    is_pause = False
    try:
        tn = telnetlib.Telnet(host=HOST, port=PORT)
        print("create connection successful")
        while True:
            num = get_wget_pros_num()
            print("num = %s" % num)
            if (not is_pause) and num > 20:
                tn.write("engine.pause()\n".encode('ascii'))
                is_pause = True
                print("engine.pause()")

            elif is_pause and num < 5:
                tn.write("engine.unpause()\n".encode('ascii'))
                is_pause = False
                print(tn.read_all().decode('ascii'))
                print("engine.unpause()")

            time.sleep(1)
    except Exception as e:
        print(e, "\n\n----Please start scrapy first----\n")


if __name__ == '__main__':
    main()
