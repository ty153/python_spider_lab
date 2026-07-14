import scrapy
from news_scrapy.items import NewsScrapyItem

class NewSpider(scrapy.Spider):
    name = "new"
    allowed_domains = ["news.163.com"]
    start_urls = ["https://news.163.com"]

    
    def parse(self, response): 
        title_elements = response.xpath('//div[@class="data_row news_article clearfix "]')
        seen = set()
        for title_elem in title_elements:
            item = NewsScrapyItem()
            title = title_elem.xpath('./div/div[1]/h3/a/text()').get()
            if title not in seen:
                item['title'] = title
                seen.add(title)
                print(f"提取到新闻: {title}")
                yield item
        

