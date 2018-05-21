# -*- coding: utf-8 -*-
import json

import scrapy
from urllib.parse import urljoin

from apks.items import ApksItem
import redis


class ApkmonkSpider(scrapy.Spider):
    name = 'apkmonk'
    allowed_domains = ['apkmonk.com']
    start_urls = ['https://www.apkmonk.com/category/action/1/']
    base_url = 'https://www.apkmonk.com/category/action/{0}/'
    current_page = 1
    # loop = asyncio.get_event_loop()
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

    # name = scrapy.Field()
    # click_url = scrapy.Field()
    # json_url = scrapy.Field()
    # download_url = scrapy.Field()

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

            # dir = name.split(".")[1][0]
            # self.logger.info("".join(['proxychains', ' wget', ' -nH', " %s" % download_url, ' -O', " %s/%s.apk" % (dir, name)]))


            # task = [async_download(name, download_url)]

            # self.loop.run_until_complete(asyncio.wait(task))
            # self.loop.close()
            # subprocess.call(['proxychains', 'wget', '-nH', "%s" % download_url, '-O', "%s/%s.apk" % (dir, name)])

            # download(name, download_url)
            # asyncDownload(name, download_url)
        except Exception as e:
            print(e)
