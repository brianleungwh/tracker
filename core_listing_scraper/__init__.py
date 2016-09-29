import subprocess
import json
import redis

r = redis.StrictRedis(host='redis', port=6379, db=0)

PYTHON = 'python'
MAIN_SCRAPY_SCRIPT = 'core_listing_scraper/initiate_spider.py'

def get_current_listings(results_page_url):
    subprocess.call([PYTHON, MAIN_SCRAPY_SCRIPT, results_page_url])
    data = {}
    listings = json.loads(r.get(results_page_url), encoding='utf-8')
    for listing in listings:
            data[listing['craig_id']] = {
                'title': listing['title'],
                'price': listing['price'],
                'absolute_url': listing['absolute_url'],
                'last_modified_at': listing['last_modified_at']
            }
    return data
