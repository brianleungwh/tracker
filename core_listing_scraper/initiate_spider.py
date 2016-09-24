import os, sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from core_listing_scraper.spiders.listing_spider import ListingSpider


results_page_url = sys.argv[1]
settings = get_project_settings()

# http://stackoverflow.com/questions/25170682/running-scrapy-from-script-not-including-pipeline
os.environ['SCRAPY_SETTINGS_MODULE'] = 'core_listing_scraper.settings'
settings_module_path = os.environ['SCRAPY_SETTINGS_MODULE']
settings.setmodule(settings_module_path, priority='project')

def fetch_data_and_write_to_file():
    process = CrawlerProcess(settings)
    process.crawl(ListingSpider, results_page_url=results_page_url)
    process.start()

if __name__ == '__main__':
    fetch_data_and_write_to_file()
