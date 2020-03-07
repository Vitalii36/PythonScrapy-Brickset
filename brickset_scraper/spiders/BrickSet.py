import scrapy
import re
from scrapy import Request

class BrickSetSpider(scrapy.Spider):
    # my cookies file for pass capcha
    name = "bricksetspider"
    start_urls = ['https://brickset.com/sets/year-2020']

    def start_requests(self):
        s = '__cfduid=d2f865bab89426a2e3dcc457301515e511583597682; cf_clearance=aedbe59de154f902d67a7608c999b0a23af5449c-1583606045-0-250; ActualCountry=CountryCode=UA&CountryName=Ukraine; PreferredCountry2=CountryCode=UA&CountryName=Ukraine; _ga=GA1.2.10857489.1583606049; _gid=GA1.2.1871067907.1583606049; playwirePageViews=7; pwUID=530598786508936; __atuvc=7%7C10; __atuvs=5e63e92480127b29006; __qca=P0-446129146-1583606052837; __gads=ID=5b6555c0ddbfe64f:T=1583606053:S=ALNI_MaHLx2sfNnlGjr02pSZ4-iCcQ5bFQ; cto_bundle=TxrP719MeDY4T3JuR1lzeUhWU1FPTWdveXJzZHRoRkl0ZXhkeVl0UUVtY1dSVzJvVmZxVXVwWmlCUjNhSGJoTG1YUFo3djFwYkF6WjUxRTBWOWIwTjJWJTJCJTJGVDJpYWlqY0olMkY0eG0zbHducmdKZXo0VzVCc0M5ZlZhU2RNUmE5QnJ3SEI0SWRhSWhGdVh4M0d5cHVmVGo2dm0xN0ElM0QlM0Q; ASP.NET_SessionId=2husbckyrulrdrjykvv5jl1e; _cmpQcif3pcsupported=1'
        s = re.split(';', s)
        mycookies = {}
        for i in s:
            i = re.split('=', i, 1)
            mycookies.update({i[0]: i[1]})

        yield scrapy.Request(url='https://brickset.com/sets/year-2020', callback=self.parse, cookies = mycookies)

    def parse(self, response):
        SET_SELECTOR = '.set'
        for brickset in response.css(SET_SELECTOR):
            # потрібно внести правки відносно приклада !!!!
            # select the correct class for the code and set name
            # NAME_SELECTOR = 'h1 a::text'
            NAME_SELECTOR = 'h1 ::text'
            PIECES_SELECTOR = './/dl[dt/text() = "Pieces"]/dd/a/text()'
            MINIFIGS_SELECTOR = './/dl[dt/text() = "Minifigs"]/dd[2]/a/text()'
            # article.set:nth-child(1) > div:nth-child(3) > div:nth-child(4) > dl:nth-child(1) > dd:nth-child(4) > a:nth-child(1)
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
            