import scrapy
from scrapy.selector import Selector


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['m.maoyan.com']
    start_urls = ['https://m.maoyan.com/films?showType=3']

    def start_requests(self):
        url = 'https://m.maoyan.com/films?showType=3'
        yield scrapy.Request(url=url, callback=self.parse, dont_filter=False)

    def parse(self, response):
        items = []
        movies = Selector(response=response).xpath('//div[@class="movie-info"]')
        for movie in movies:

            film_title = movie.xpath('./div[@class="title line-ellipsis"]/text()')
            film_type = movie.xpath('./div[@class="actors line-ellipsis"]/text()')
            film_time = movie.xpath('./div[@class="show-info line-ellipsis"]/text()')

            items.append({'title' : film_title.extract_first().strip(), 'type' : film_type.extract_first().strip(), 'time' : film_time.extract_first().strip()[0:10]})

        return items
