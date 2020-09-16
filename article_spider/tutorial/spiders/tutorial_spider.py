import scrapy
from scrapy.pipelines.files import FilesPipeline
from tutorial.items import articleitem
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import random
import time
class demo_spider(scrapy.Spider):
    name = "info"
    #name2title = dict()
    cookie = 'JSESSIONID=ABAAABAAAFCAAEG34858C57541C1F9DF75AED18C3065736; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1524281748;  04797acf-4515-11e8-90b5- LGSID=20180421130026-e7e614d7-4520-PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_python%3Fcity%3D%25E6%25B7%25B1%25E5%259C%25B3%26cl%3Dfalse%26fromSearch%3Dtrue%26labelWords%3D%26suginput%3D; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2F4302345.html; LGRID=20180421130208-24b73966-4521-11e8-90f2-525400f775ce; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1524286956'
    headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
               'Referer': 'https://www.lagou.com/jobs/list_python?city=%E6%B7%B1%E5%9C%B3&cl=false&fromSearch=true&labelWords=&suginput=',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
               'cookie': cookie }
    def start_requests(self):   
        excel = pd.read_excel('E://大创//test.xlsx')
        urls = list(excel['url'])
        #ieeelist=[]
        for i in range(len(urls)):
            if excel.loc[i, 'platform'] == 'scholar':
                yield scrapy.Request(url=urls[i], callback=self.scholar1, headers=self.headers, meta={'author': excel.loc[i, 'author']})
        for i in range(len(urls)):
            if excel.loc[i, 'platform'] == 'mendeley':
                yield scrapy.Request(url=urls[i], callback=self.mendeley1, headers=self.headers, meta={'author': excel.loc[i, 'author']})
        for i in range(len(urls)):
            if excel.loc[i, 'platform'] == 'cnki':
                yield scrapy.Request(url=urls[i], callback=self.cnki1, headers=self.headers, meta={'author': excel.loc[i, 'author']})
        for i in range(len(urls)):
            if excel.loc[i, 'platform'] == 'ieee':
               yield scrapy.Request(url=urls[i], callback=self.simulate1, headers=self.headers, meta={'author': excel.loc[i, 'author']})
        for i in range(len(urls)):
            if excel.loc[i, 'platform'] == 'acm':
                urls[i] = urls[i] + '/publications?Role=author'
                yield scrapy.Request(url=urls[i], callback=self.parse1, headers=self.headers, meta={'author': excel.loc[i, 'author']})
        
            
    def parse1(self, response):
        author=response.meta['author']
        if response.url.find('acm') != -1:
            for url in response.xpath('//span[@class="hlFld-Title"]/a/@href').extract():
                url = 'https://dl.acm.org' + url
                yield scrapy.Request(url=url, callback=self.acm2, headers=self.headers, meta={'author': author})
                time.sleep(random.randint(1,3))
            for nexthref in response.xpath('//nav[@class="pagination"]/span/a[@title="Next Page"]/@href').extract():
                yield scrapy.Request(url=nexthref, callback=self.parse1, headers=self.headers, meta={'author': author})
        

    def acm2(self, response):
        item = articleitem()
        item['author'] = response.meta['author']
        item['title'] = response.xpath('//h1[@class="citation__title"]/text()').extract()[0]
        item['abstract'] = response.xpath('//div[@class="abstractSection abstractInFull"]/p/text()').extract()[0]
        item['platform'] = 'acm'
        yield item
        time.sleep(random.randint(3, 5))

    def simulate1(self,response):
        browser = webdriver.Edge()
        browser.get(response.url)
        urls=[]
        explicit_wait = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH,'//xpl-paginator'))
        )
        while True:
            tags = browser.find_elements_by_xpath('//div[@class="col result-item-align"]/h2/a')
            for tag in tags:
                urls.append(tag.get_attribute('href'))
            button = browser.find_elements_by_xpath('//li[@class="next-btn"]/a')
            if button:
                button[0].click()
                explicit_wait = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.XPATH,'//xpl-paginator'))
                )
            else:
                break
        browser.close()
        for url in urls:
            browser = webdriver.Edge()
            browser.get(url)
            explicit_wait = WebDriverWait(browser, 20).until(
                EC.presence_of_element_located((By.XPATH,'//div[@class="footer-wrapper"]'))
            )
            item=articleitem()
            titletag = browser.find_element_by_xpath('//h1[@class="document-title"]/span')
            item['title'] = titletag.text
            abstractag = browser.find_element_by_xpath('//div[@class="u-mb-1"]/div')
            item['abstract'] = abstractag.text
            item['author'] = response.meta['author']
            item['platform']='ieee'
            yield item
            browser.close()
        
    def cnki1(self, response):
        browser = webdriver.Edge()
        browser.get(response.url)
        explicit_wait = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="frame3"]'))
        )
        iframe = browser.find_element_by_name('frame3')
        browser.switch_to.frame(iframe)
        tags = browser.find_elements_by_xpath('//ul[@class="bignum"]/li/a[@target="kcmstarget"]')
        for tag in tags:
            yield scrapy.Request(url=tag.get_attribute('href'), callback=self.cnki2, meta={'author': response.meta['author']})
        browser.close()
    
    def cnki2(self, response):
        try:
            item = articleitem()
            item['title'] = response.xpath('//div[@class="wx-tit"]/h1/text()').extract()[0]
            item['abstract'] = response.xpath('//span[@class="abstract-text"]/text()').extract()[0]
            item['author'] = response.meta['author']
            item['platform'] = 'cnki'
            yield item
            time.sleep(random.randint(1, 3))
        except IndexError:
            pass
        
    def mendeley1(self, response):
        browser = webdriver.Edge()
        browser.get(response.url)
        time.sleep(15)
        browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        while True:
            try:
                button = browser.find_element_by_xpath('//footer[@class="publications-footer"]/div/button')
                button.click()
                time.sleep(10)
                browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            except:
                break
        tags = browser.find_elements_by_xpath('//h2[@class="TitlePrimary-u64kwp-0 egVvbs"]/a')
        for tag in tags:
            yield scrapy.Request(url=tag.get_attribute('href'), callback=self.mendeley2, meta={'author': response.meta['author']})
        browser.close()

    def mendeley2(self, response):
        item = articleitem()
        item['title'] = response.xpath('//*[@id="root"]/div/div[1]/div/div/div/div[1]/div/div/div[1]/h1/text()').extract()[0]
        item['abstract'] = response.xpath('//*[@id="root"]/div/div[2]/div/div[1]/div[1]/p/span/text()').extract()[0]
        item['author'] = response.meta['author']
        item['platform'] = 'mendeley'
        yield item
        time.sleep(random.randint(3, 5))
    
    def scholar1(self, response):
        urls = response.xpath('//td[@class="gsc_a_t"]/a/@data-href').extract()
        for url in urls:
            url='https://scholar.google.co.jp/'+url
            yield scrapy.Request(url=url, callback=self.scholar2, meta={'author': response.meta['author']})
            time.sleep(random.randint(1,3))
    
    def scholar2(self, response):
        try:
            item = articleitem()
            item['title'] = response.xpath('//div[@id="gsc_vcd_title"]/a/text()').extract()[0]
            abstract = response.xpath('//div[@class="gsh_csp"]/text()').extract()
            if abstract:
                item['abstract'] = abstract[0]
            else:
                item['abstract']=response.xpath('//div[@class="gsh_small"]/text()').extract()[0]
            item['author'] = response.meta['author']
            item['platform'] = 'scholar'
            yield item
            time.sleep(random.randint(3, 5))
        except IndexError:
            pass