# -*- coding: utf-8 -*-
import json
import redis
import scrapy
from urllib.parse import urljoin
from apks.items import ApksItem


class ApkmonkSpider(scrapy.Spider):
    name = 'apkmonk'
    allowed_domains = ['apkmonk.com']
    start_urls = ['https://www.apkmonk.com/category/action/1/']
    base_url = 'https://www.apkmonk.com/category/action/{0}/'
    current_page = 1
    pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
    r = redis.Redis(connection_pool=pool)

    def parse(self, response):
        urls = response.xpath('//*[@class="row"]//a/@href').extract()
        urls = set(urls)
        urls = list(urls)
        for url in urls:
            url = urljoin(response.url, url)
            yield scrapy.Request(url, callback=self.parse_click)

        self.current_page += 1
        next_page = self.base_url.format(self.current_page)
        yield scrapy.Request(next_page, callback=self.parse)

    def parse_click(self, respone):
        click_url = respone.xpath('//*[@id="download_button"]/@href').extract_first()
        name, key = click_url.split("/")[-3:-1]
        json_url = urljoin(respone.url, "/down_file/?pkg={0}&key={1}".format(name, key))
        meta = {
            'name': name,
            'click_url': click_url,
        }
        yield scrapy.Request(json_url, meta=meta, callback=self.getDownloadJs)

    def getDownloadJs(self, response):
        re_json = json.loads(response.text)
        try:
            download_url = re_json["url"]
            json_url = response.url
            name = response.meta.get("name")
            item = ApksItem()
            item["name"] = name
            item['click_url'] = response.meta.get("click_url")
            item['json_url'] = json_url
            item['download_url'] = download_url

            value = name + "," + download_url
            self.r.lpush("apks", value)
            yield item
        except Exception as e:
            print(e)
