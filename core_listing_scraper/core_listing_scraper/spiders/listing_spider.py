import scrapy
from scrapy.loader import ItemLoader
from core_listing_scraper.items import CraigslistItem

CRAIGSLIST_PAGINATION_LIMIT = 24

TEST_URL = 'http://losangeles.craigslist.org/search/cta?query=135i&auto_transmission=1'

class ListingSpider(scrapy.Spider):
    name = 'listing_spider'

    def __init__(self, results_page_url=):
        super(ListingSpider, self).__init__()
        self.start_urls = self._build_start_urls(results_page_url=TEST_URL)
        self.hostname = results_page_url.split('search')[0][:-1]
        
    @staticmethod
    def _build_start_urls(initial_results_page_url):
        urls = [initial_results_page_url]
        has_query_params = "?" in initial_results_page_url
        for i in range(1, CRAIGSLIST_PAGINATION_LIMIT):
            pagination = i * 100
            if has_query_params:
                pagination_param = "&s={param}".format(param=pagination)
            else:
                pagination_param = "?s={param}".format(param=pagination)
            urls.append(initial_results_page_url + pagination_param)
        return urls

    def parse(self, response):
        listings = response.xpath(".//p")
        # . selects the current node
        # // elects nodes in the document from the current node that match the selection no matter where they are
        for listing in listings:
            item = CraigslistItem()
            self.make_item(listing, item)
            yield item

    def make_item(self, listing, item):
        item['craig_id'] = listing.xpath("@data-pid").extract_first()
        item['absolute_url'] = self.hostname + listing.xpath("a/@href").extract_first()
        listing_info = listing.xpath("span[@class='txt']")
        item['last_modified_at'] = listing_info.xpath("span[@class='pl']/time/@datetime").extract_first()
        title_tag = listing_info.xpath("span[@class='pl']/a/span[@id='titletextonly']")
        item['title'] = title_tag.xpath("text()").extract_first()
        price_tag = listing_info.xpath("span[@class='l2']/span[@class='price']")
        item['price'] = price_tag.xpath("text()").extract_first()
