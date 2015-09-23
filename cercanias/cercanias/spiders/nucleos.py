# -*- coding: utf-8 -*-
import scrapy
from cercanias.items import NucleosItem 


class NucleosSpider(scrapy.Spider):
    name = "nucleos"
    allowed_domains = ["http://www.renfe.com/viajeros/cercanias/"]
    start_urls = (
        'http://www.http://www.renfe.com/viajeros/cercanias/',
    )

    def parse(self, response):

        # Get nucleos by columns
        for nucleo_link in response.xpath('//div[@id="colB"]/div[@class="colB1"]'):
            pass



        """
        for nucleo_link in response.xpath('//div[@id="menu_lat"]/ul/li/a/@href').extract():

            if nucleo_link == 'http://cercanias.blog.renfe.com/':
                continue

            nucleo_url = response.urljoin(nucleo_link)

            yield scrapy.Request(nucleo_url, callback=self.parse_nucleo_url)

    def parse_nucleo_url(self, response)
        pass
    """
