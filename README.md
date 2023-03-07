# Amazon-data-scrapper
## About
The goal of this project is trying to get a list of all laptop products appearing on the amazon e-commerce webpage, and then sequentially scrape
details about the configuration for each laptop model.

The project is developed using scrapy framework - a fast high-level web crawling and web scraping framework used to crawl websites and extract structured data from their pages.

## How does it run
There are two spiders. One for collecting all laptop names and general information. One for going to detail about each laptop

With the second one, the waiting time for complete data might take 5 hours long (depending on the Internet), and there can be any unexpected failure during the
scraping task. So to keep the data persistent, there is a file name progress.json to store the scraping status for each product in the
laptop list.

During the scraping process, the spider may encounter 503 Service Unavailable (because amazon flagged the spider as a scraper and is blocking requests from your spider.). Configuring the middleware helps me handle this by making every request to the server be attached with a different user agent's name.

## How to run
- Step 1: run 

`scrapy crawl laptop_list -O laptop_list.csv --logfile log_laptop_list.log -a list_max_len=5`

the list_max_len is optional!

- Step 2: run

`scrapy crawl laptop_detail -O laptop_detail.json --logfile log_laptop_detail.log`

Whenever a failure occurs, it will be saved for the next try and skipped. You might have to run this command a couple of times to make sure
the program ends with the message "DONE"
