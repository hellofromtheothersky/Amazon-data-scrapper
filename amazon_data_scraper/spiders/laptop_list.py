import scrapy
from bs4 import BeautifulSoup
import numpy as np


class LaptopListSpider(scrapy.Spider):
    name = 'laptop_list'
    allowed_domains = ['amazon.com']
    start_urls = ['https://www.amazon.com/s?i=computers-intl-ship&bbn=16225007011&rh=n%3A16225007011%2Cn%3A13896617011%2Cn%3A565108&dc&ds=v1%3Ao%2FINkIAqqX2QGX%2BkttIg8PsqJF1NC156Qv6yTuGhATA&qid=1668504788&rnid=13896617011&ref=sr_nr_n_2']

    def parse(self, response):
        def extract_text(p, selector):
            rs=[]
            for x in p:
                try:
                    rs.append(x.select_one(selector).text.strip())
                except AttributeError:
                    rs.append(np.nan) 
            return rs

        soup=BeautifulSoup(response.text, features='lxml')
        domain='https://www.amazon.com'

        widget=soup.select('.s-card-container')
        tittle=[x.select_one('.s-card-container h2 a').text for x in widget]
        link=[domain+x.select_one('h2 a').get('href') for x in widget]
        # might be not found
        price=extract_text(widget, 'span.a-price-whole')
        old_price=extract_text(widget, 'span.a-price.a-text-price span.a-offscreen')

        item=dict()
        for laptop in list(zip(tittle, price, old_price, link)):
                item['name']= laptop[0]
                item['price']= laptop[1]
                item['old_price']= laptop[2]
                item['link']= laptop[3]
                yield item
        
        next_page=soup.select_one('.s-pagination-next').get('href')
        if next_page:
            print('Going to next page')
            yield response.follow(domain+next_page, callback=self.parse)
    print('Complete')
