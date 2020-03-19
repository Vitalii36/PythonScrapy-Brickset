import scrapy
import re
from scrapy import Request
from brickset_scraper.mycookiescapcha.mycookies import mycook

class BrickSetSpider(scrapy.Spider):
    name = "bricksetspider"
    start_urls = ['https://brickset.com/sets/year-2020']

    # my cookies file for pass capcha
    def start_requests(self):
        cook = mycook()
        yield scrapy.Request(url='https://brickset.com/sets/year-2020', callback=self.parse, cookies=cook)

    def parse(self, response):
        SET_SELECTOR = '.set'
        for brickset in response.css(SET_SELECTOR):
            # select the correct class for the code and set name
            NAME_SELECTOR = 'h1 ::text'
            PIECES_SELECTOR = './/dl[dt/text() = "Pieces"]/dd/a/text()'
            MINIFIGS_SELECTOR = './/dl[dt/text() = "Minifigs"]/dd[2]/a/text()'
            IMAGE_SELECTOR = 'img ::attr(src)'
            yield {
                'name': brickset.css(NAME_SELECTOR).extract_first(),
                'pieces': brickset.xpath(PIECES_SELECTOR).extract_first(),
                'minifigs': brickset.xpath(MINIFIGS_SELECTOR).extract_first(),
                'image': brickset.css(IMAGE_SELECTOR).extract_first(),
            }

            NEXT_PAGE_SELECTOR = '.next a ::attr(href)'
            next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
            if next_page:
                yield scrapy.Request(
                    response.urljoin(next_page),
                    callback=self.parse
                )
            