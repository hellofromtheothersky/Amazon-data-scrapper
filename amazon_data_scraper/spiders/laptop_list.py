import scrapy
from bs4 import BeautifulSoup
import numpy as np


class LaptopListSpider(scrapy.Spider):
    name = 'laptop_list'
    allowed_domains = ['amazon.com']
    start_urls = ['https://www.amazon.com/s?i=computers-intl-ship&bbn=16225007011&rh=n%3A16225007011%2Cn%3A13896617011%2Cn%3A565108&dc']
    list_cur_len=0

    def __init__(self, list_max_len):
        if list_max_len:
            self.list_max_len=int(list_max_len)
        else:
            self.list_max_len=9999

    def parse(self, response):
        def extract_text(p, selector):
            rs=[]
            for x in p:
                try:
                    rs.append(x.select_one(selector).text.strip())
                except AttributeError:
                    rs.append(np.nan) 
            return rs
        print(self.list_max_len)
        soup=BeautifulSoup(response.text, features='lxml')
        domain='https://www.amazon.com'

        widget=soup.select('.s-card-container')
        tittle=[x.select_one('.s-card-container h2 a').text for x in widget]
        link=[domain+x.select_one('h2 a').get('href') for x in widget]
        # might be not found
        price=extract_text(widget, 'span.a-price-whole')
        old_price=extract_text(widget, 'span.a-price.a-text-price span.a-offscreen')
        next_page=soup.select_one('.s-pagination-next').get('href')

        item=dict()
        
        for laptop in list(zip(tittle, price, old_price, link)):
            item['name']= laptop[0]
            item['price']= laptop[1]
            item['old_price']= laptop[2]
            item['link']= laptop[3]
            self.list_cur_len+=1
            yield item

            if self.list_cur_len==self.list_max_len:
                next_page=False
                break
        
        if next_page:
            print('Going to next page')
            yield response.follow(domain+next_page, callback=self.parse)
