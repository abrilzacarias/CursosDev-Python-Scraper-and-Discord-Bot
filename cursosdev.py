from scrapy.item import Field, Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess
import schedule
import time
import json
import os

class Courses(Item):
    name = Field()
    creator = Field()    
    url = Field()


class CursosDevCrawler(CrawlSpider):
    name = 'cursosdev'
    allowed_domains = ['cursosdev.com']
    start_urls = ['https://www.cursosdev.com/']

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'LOG_LEVEL': 'DEBUG'
    }

    download_delay = 1

    rules = (
        #pagination
        Rule(
            LinkExtractor(allow=r'/?page=[1-5]'), 
                        follow=True),
        #items
        Rule(
            LinkExtractor(allow=r'/coupons-udemy/'),
            follow=True, callback='parse_items'),
        )
    
    def __init__(self, *args, **kwargs):
        super(CursosDevCrawler, self).__init__(*args, **kwargs)
        self.courses = []
    

    def parse_items(self, response):
        self.logger.info('Parsing items from: %s', response.url)
    
        # Obtener los datos directamente con XPath
        name = response.xpath('/html/body/main/div[1]/div[1]/div[2]/article/div/header/h3/a/text()').get()
        creator = response.xpath('/html/body/main/div[1]/div[1]/div[2]/article/div/footer/div[1]/a[2]/text()').get()
        url = response.xpath('/html/body/main/div[1]/div[1]/div[3]/div/div/div[4]/div/div/a[1]/@href').get()
        
        # Crear el diccionario del curso
        item = {
            'name': name,
            'creator': creator,
            'url': url
        }
        
        self.courses.append(item)
        #self.logger.debug('Course found: %s', item)
    
    def closed(self, reason):
        self.logger.info('Spider closed: %s. Saving data to courses.json.', reason)
        with open('courses.json', 'w', encoding='utf-8') as f:
            json.dump(self.courses, f, ensure_ascii=False, indent=4)
        self.logger.info('Data saved successfully.')


def run_scraper():
    process = CrawlerProcess()
    process.crawl(CursosDevCrawler)
    process.start()

def scrape_if_empty():
    if not os.path.exists('courses.json') or os.stat('courses.json').st_size == 0:
        print("JSON file is empty or does not exist. Running scraper...")
        run_scraper()
    else:
        print("JSON file exists and is not empty. No need to scrape.")

# Schedule the scraper to run twice a day
schedule.every().day.at("06:00").do(run_scraper)
schedule.every().day.at("18:05").do(run_scraper)

def start_scheduler():
    print("Scheduler is running...")
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    # Run the scraper manually if desired
    print("Running scraper manually...")
    run_scraper()



