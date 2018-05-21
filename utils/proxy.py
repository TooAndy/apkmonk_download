#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'aniss'
import requests


def get_proxy():
    proxy = str(requests.get("http://35.229.218.162:5010/get/").content)[2:-1]
    proxy = "http://" + proxy
    return proxy


def delete_proxy(proxy):
    requests.get("http://http://35.229.218.162:5010/delete/?proxy={0}".format(proxy))
