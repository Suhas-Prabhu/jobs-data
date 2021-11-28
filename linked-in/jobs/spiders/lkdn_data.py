import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd
import datetime
from scrapy.utils.response import open_in_browser

class YSpider(scrapy.Spider):
    name = "lkdn"
    data = pd.read_csv('data/lnpages.csv')
    start_urls = data['Urls'].to_list()
    t = datetime.datetime.now().strftime("%Y-%m-%d")
    custom_settings = { 
                       'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36' ,
                       'FEED_FORMAT': 'csv',
                       'FEED_URI': 'lkdn_data_{}.csv'.format(t),
                       'DOWNLOAD_DELAY':1,
                       'AUTOTHROTTLE_ENABLED': True}
    
           
    def parse(self, response):
      url = response.xpath('/html/body/div[6]/div[3]/div[3]/div[2]/div/section/div/div/ul/li/div/div/div/div[2]/div[1]/a/@href').extract()
      print(url)

      
if __name__ == "__main__":
  process = CrawlerProcess()
  process.crawl(YSpider)
  process.start()