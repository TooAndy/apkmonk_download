# -*- coding: utf-8 -*-
# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import logging
from scrapy import signals
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.http import HtmlResponse
from scrapy.utils.response import response_status_message



class ApksSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ApksDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class Selenium_middleware(object):
    def process_request(self, request, spider):
        if request.meta.get('chromedriver'):
            print("访问:{0}".format(request.url))
            spider.browser.get(request.url)
            # findElement(By.tagName("body")).sendKeys("Keys.ESCAPE");
            # while True:
            #     if spider.browser.find_elements_by_xpath('//*[@id="download_sub_text"]/a/@href'):
            #         spider.browser.send_keys
            #         # selenium.webdriver.common.action_chains.ActionChains#send_keys

            return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source, request=request,
                                encoding='utf-8')


class MyRetryMiddleware(RetryMiddleware):
    logger = logging.getLogger(__name__)

    # delete proxy from proxies pool
    def delete_proxy(self, request):
        try:
            proxy = request.meta['proxy'].replace("http://", "")
            self.logger.info("删除无用代理： %s" % request.meta['proxy'])
            # print("删除无用代理：", request.meta['proxy'])
        except Exception as e:
            print("删除代理出错: ", e)

    def process_response(self, request, response, spider):
        if response.status in {400, 401, 402, 403}:
            print("------------------------------------------\n", response.status,
                  "\n------------------------------------------\n")
        if request.meta.get('dont_retry', False):
            return response
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            # 删除该代理
            self.delete_proxy(request)
            self.logger.warning('返回值异常, 进行重试...')
            return self._retry(request, reason, spider) or response
        return response

    def process_exception(self, request, exception, spider):

        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) \
                and not request.meta.get('dont_retry', False):
            # 删除该代理
            self.delete_proxy(request)
            self.logger.warning('连接异常, 进行重试...')

            return self._retry(request, exception, spider)


class MyproxiesSpiderMiddleware(object):
    logger = logging.getLogger(__name__)

    def process_request(self, request, spider):
        if "proxy" not in request.meta.keys():
            # proxy = get_proxy()
            proxy = "10.104.2.219:8087"
            self.logger.info("使用代理ip： %s" % proxy)
            request.meta["proxy"] = proxy

    def process_response(self, request, response, spider):
        if response.status in {400, 401, 402, 403}:
            print("------------------------------------------\n", response.status,
                  "\n------------------------------------------\n")

        """检查response.status，根据status是否在允许的状态码中决定是否切换到下一个proxy，或者禁用proxy"""
        if 'proxy' in request.meta.keys():
            self.logger.debug('%s %s %s' % (request.meta['proxy'], response.status, request.url))
        else:
            self.logger.debug('None %s %s' % (response.status, request.url))

        # status不是正常的200而且不在spider声明的正常爬取过程中可能出现的
        # status列表中，则认为代理无效，切换代理
        if response.status != 200:
            self.logger.info('response status not in spider.website_possible_httpstatus_list')

            new_request = request.copy()
            new_request.dont_filter = True
            return new_request
        else:
            return response
