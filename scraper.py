from scrapy.item import Field, Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess
from config import connection

class Courses(Item):
    name = Field()
    creator = Field()    
    url = Field()


class CursosDevCrawler(CrawlSpider):
    def __init__(self, *args, **kwargs):
        super(CursosDevCrawler, self).__init__(*args, **kwargs)
        self.courses = []
        
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
            LinkExtractor(allow=r'/?page=[1-3]'), 
                        follow=True),
        #items
        Rule(
            LinkExtractor(allow=r'/coupons-udemy/'),
            follow=True, callback='parse_items'),
        )
    

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
        self.saveToDb(item)

    def saveToDb(self, item):
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO course (name, creator, url) VALUES (%s, %s, %s)"
                cursor.execute(sql, (item['name'], item['creator'], item['url']))
            connection.commit()
        except Exception as e:
            self.logger.error(f"Error saving to database: {e}")

def run():
    process = CrawlerProcess()
    process.crawl(CursosDevCrawler)
    process.start()

if __name__ == "__main__":
    # Run the scraper manually if desired
    print("Running scraper manually...")
    run()



