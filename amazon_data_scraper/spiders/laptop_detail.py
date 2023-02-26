import scrapy
import json
from bs4 import BeautifulSoup
import pandas as pd

class LaptopLinksProgress:
    def __init__(self, new_progress):  # set new_progress=True if want to reset current progress data
        if new_progress == 'True':
            self.create_new_progress()
        with open("progress.json", "r") as rf:
            self.progress = json.load(rf)
        self.first_undone = 0
        self.update_first_undone()

    def create_new_progress(self):
        laptop_overview = pd.read_csv("laptop_list.csv")
        links = laptop_overview["link"].to_list()
        progress = list(zip(links, [0] * len(links)))
        with open("progress.json", "w") as wf:
            json.dump(progress, wf)

    def update_first_undone(self):
        pos=self.first_undone
        n=len(self.progress)
        for i in range(pos, n+1):
            if i==n:
                self.first_undone = -1
                break
            if self.progress[i][1] == 0: 
                self.first_undone = i
                break
        

    def get_first_undone_link(self):
        if self.first_undone>=0 and self.first_undone<len(self.progress):
            return self.progress[self.first_undone][0]
        else:
            return None

    def done_first_undone_link(self):
        self.progress[self.first_undone][1] = 1
        self.update_first_undone()
        with open("progress.json", "w") as wf:
            json.dump(self.progress, wf)

    def skip_first_undone_link(self):
        self.first_undone+=1
        self.update_first_undone()

    def status(self):
        return "{}/{}".format(self.first_undone+1, len(self.progress))

class LaptopDetailSpider(scrapy.Spider):
    name = "laptop_detail"
    allowed_domains = ["amazon.com"]
    def __init__(self, new_progress=False):
        self.progress=LaptopLinksProgress(new_progress)
        self.start_urls = [self.progress.get_first_undone_link()]


    def parse(self, response):
        print("Scrape ", self.progress.status(), self.progress.get_first_undone_link())

        soup = BeautifulSoup(response.text, features="lxml")
        #available data table
        detail = soup.select("div.a-row.a-spacing-top-base tr")
        criterion = [x.select_one("th").text.strip() for x in detail]
        info = [x.select_one("td").text.strip() for x in detail]
        data = dict(zip(criterion, info))
        #link
        data["link"] = self.progress.get_first_undone_link()
        data['official link']=response.url
        #description
        try:
            description_info = soup.select_one("div#productDescription")
            description_info = description_info.get_text("###")
        except:
            pass
        else:
            data["description"] = description_info.strip()

        if len(detail)==0: 
            self.progress.skip_first_undone_link()
            print('Skip')
        else:
            self.progress.done_first_undone_link()
            print('Done')
            yield data

        next_link=self.progress.get_first_undone_link()
        if next_link:
            yield response.follow(next_link, callback=self.parse)
