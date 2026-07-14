# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from fake_useragent import UserAgent
import time
import random
from scrapy.http import HtmlResponse

class NewsScrapySpiderMiddleware:
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

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    async def process_start(self, start):
        # Called with an async iterator over the spider start() method or the
        # maching method of an earlier spider middleware.
        async for item_or_request in start:
            yield item_or_request

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class NewsScrapyDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')# 让 Chrome 使用 CPU 渲染页面，而不是 GPU
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')# 隐藏自动化特征
        ua = UserAgent().chrome
        chrome_options.add_argument(f'--user-agent={ua}')
        
        service = Service(r'D:\pycharm\python\chromedriver.exe')
        s.driver = webdriver.Chrome(service=service, options=chrome_options)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s
    
            
    def process_request(self, request, spider):
        if spider.name != "new":
            return None
        self.driver.get(request.url)
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        i = 0
        count = 10
        while True:
            i+=1
            print(f"第{i}次加载页面")
            # 滚动页面
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

            # 等待加载出来
            time.sleep(random.uniform(2, 4))

            # 找到“加载更多”按钮并点击
            try:
                load_more_btn = WebDriverWait(self.driver,5).until(
                EC.presence_of_element_located((By.XPATH, '//*[contains(text(),"加载更多")]'))
            )
            
                self.driver.execute_script('arguments[0].click();', load_more_btn)
            except Exception:
                print("没有找到'加载更多'按钮，尝试判断是否已加载完...")
            
            # 判断是否加载完成
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                print("页面高度不再变化，加载完成")
                break
            # 更新last_height
            last_height = new_height
            

        return HtmlResponse(
            url = request.url,
            body = self.driver.page_source,
            encoding = 'utf-8',
            request = request
        )
                    

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
        spider.logger.info("Spider opened: %s" % spider.name)

    def spider_closed(self, spider):
        if hasattr(self, 'driver'):
            self.driver.quit()