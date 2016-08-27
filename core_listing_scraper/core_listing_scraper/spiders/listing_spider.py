import scrapy
from scrapy.loader import ItemLoader
from scrapy.utils.url import urljoin_rfc
from scrapy.utils.response import get_base_url
from core_listing_scraper.items import CraigslistItem

CRAIGSLIST_PAGINATION_LIMIT = 24

TEST_URL = 'http://losangeles.craigslist.org/search/cta?query=135i&auto_transmission=1'

class ListingSpider(scrapy.Spider):
    name = 'listing_spider'

    def __init__(self, results_page_url=TEST_URL):
        super(ListingSpider, self).__init__()
        self.start_urls = self._build_start_urls(results_page_url)
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
            self.make_item(response, listing, item)
            yield item

    @staticmethod
    def get_absolute_url(response, relative_url):
        return urljoin_rfc(get_base_url(response), relative_url)

    def make_item(self, response, listing, item):
        item['craig_id'] = listing.xpath("@data-pid").extract_first()
        a_href_link = listing.xpath("a/@href").extract_first()
        item['absolute_url'] = self.get_absolute_url(response, a_href_link)
        listing_info = listing.xpath("span[@class='txt']")
        item['last_modified_at'] = listing_info.xpath("span[@class='pl']/time/@datetime").extract_first()
        title_tag = listing_info.xpath("span[@class='pl']/a")
        item['title'] = title_tag.xpath("text()").extract_first()
        price_tag = listing_info.xpath("span[@class='l2']/span[@class='price']")
        item['price'] = price_tag.xpath("text()").extract_first()
