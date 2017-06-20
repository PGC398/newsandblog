import re,os
import urllib.request
import ssl
import scrapy
from sys import path
path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"../..")))
from nab.items import NabItem
from scrapy.http import Request
#from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.spiders import CrawlSpider, Rule
from scrapy import cmdline
    
class NabSpider(CrawlSpider):
        
    name = "nab"
    start_urls = ['http://taobao.com/']

    def __init__(self, url=None, *args, **kwargs):
        super(NabSpider, self).__init__(*args, **kwargs)
        self.url=url
        
    def parse(self, response):
        url=self.url
        if "news.qq" in url:
            yield Request(url=url,callback=self.tx)
        elif "news.163" in url:
            yield Request(url=url,callback=self.wy)
        elif "blog.sina" in url:
            yield Request(url=url,callback=self.blog)
        else:
            yield Request(url=url,callback=self.default)
            
    def wy(self,response):
        item = NabItem()
        content=response.xpath("//div[@class='post_text']/p/text()").extract()
        purity=sorted(set(content),key=content.index)
        try:
            purity.remove('')
        except:
            pass
        
        result=''
        for i in range(len(purity)):
            result+=purity[i]+','
        list1=[]
        list1.append(result.strip())
        item['content']=list1
        yield item

    def tx(self,response):
        item = NabItem()
        content=response.xpath("//div[@id='Cnt-Main-Article-QQ']/p/text()").extract()
        purity=sorted(set(content),key=content.index)
        try:
            purity.remove('')
        except:
            pass
        
        result=''
        for i in range(len(purity)):
            result+=purity[i]+','
        list1=[]
        list1.append(result.strip())
        item['content']=list1
        yield item

    def blog(self,response):
        item = NabItem()
        allcontent=response.xpath("//div[@id='sina_keyword_ad_area2']").extract()
        content=re.compile(r'[\u4e00-\u9fa5]*').findall(allcontent[0])
        purity=sorted(set(content),key=content.index)
        try:
            purity.remove('')
        except:
            pass
        
        result=''
        for i in range(len(purity)):
            result+=purity[i]+','
        list1=[]
        list1.append(result.strip())
        item['content']=list1
        yield item
        

    def default(self,response):
        item = NabItem()
        try:           
            asd=response.body.decode('utf-8')
        except UnicodeDecodeError:
            try:            
                asd=response.body.decode('gbk')
            except UnicodeDecodeError:
                try:
                    asd=response.body.decode('gb2312')
                except UnicodeDecodeError:
                    asd=response.body
        content=re.compile(r'[\u4e00-\u9fa5]*').findall(asd)
        purity=sorted(set(content),key=content.index)
        try:
            purity.remove('')
        except:
            pass
        
        result=''
        for i in range(len(purity)):
            result+=purity[i]+','
        list1=[]
        list1.append(result.strip())
        item['content']=list1
        yield item
        
    
    
