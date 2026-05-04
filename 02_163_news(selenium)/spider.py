from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from config import URL,get_headers
import time
import random
from lxml import etree
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def create_headless_driver():
    chrome_options = Options()
    # 无头参数配置
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    headers =get_headers()
    chrome_options.add_argument(f'--user-agent={headers["User-Agent"]}')
    
    # 实例化
    service = Service(r'D:\pycharm\python\chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def parse_news(page_source):
    """解析HTML,提取新闻标题列表"""
    if not page_source:
        print("页面源代码为空")
        return []
    
    tree = etree.HTML(page_source)
    title_elements = tree.xpath('//div[@class="data_row news_article clearfix "]')
    titles = []
    seen = set()
    for elemt in title_elements:
        title_list = elemt.xpath('./div/div[1]/h3/a/text()')
        if title_list:
            title = title_list[0].strip()
            if title and title not in seen:
                titles.append({'title': title})
                seen.add(title)
                print(f"提取到新闻: {title}")
    return titles

def crawl_news():
    driver = create_headless_driver()
    driver.get(URL) 

    # 获取初始页面高度
    last_height = driver.execute_script("return document.body.scrollHeight")
    i=0
    while True:
        i+=1
        # 1. 滚动到页面底部
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        
        # 2. 随机等待页面加载
        time.sleep(random.uniform(2, 4))
        
        # 3. 尝试点击“加载更多”按钮
        try:
             # 等待按钮出现，最多等5秒
            load_more_btn = WebDriverWait(driver,5).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='index2016_wrap']/div[3]/div[2]/div[3]/div[2]/div[5]/div/a[3]"))
            )
            driver.execute_script('arguments[0].click();', load_more_btn)
            print(f'第{i}次加载')
            time.sleep(random.uniform(1, 3))
        except:
            print("没有找到'加载更多'按钮，尝试判断是否已加载完...")
        
        # 4. 获取新的页面高度，如果高度没变，说明已到底部
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("页面高度不再变化，内容已加载完毕。")
            break
        last_height = new_height
       

    print("正在获取网页源代码...")
    page_source = driver.page_source
    driver.quit()
    
    return parse_news(page_source)
