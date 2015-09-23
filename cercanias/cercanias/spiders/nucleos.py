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
        for nucleo_div in response.xpath('//div[@id="colB"]/div[@class="colB1" or @class="colB2" or @class="colB3"]'):
            
            # Get nucleo name
            nucleo_name_array = nucleo_div.xpath('/h3/a/@title').extract()
            if not nucleo_name_array or not isinstance(nucleo_name_array, list) or len(nucleo_name_array) <= 0:
                continue


            # Get link to nucleo page
            nucleo_link_array = nucleo_div.xpath('h3/a/@href').extract()
            if not nucleo_link_array or not isinstance(nucleo_link_array, list) or len(nucleo_link_array) <= 0:
                continue

            nucleo_link = nucleo_link_array[0]

            # Follow the link to get nucleo id
            nucleo_url = response.urljoin(nucleo_link)

            # Get link to image
            nucleo_img_array = nucleo_div.xpath('p/a/img/@src').extract()

            # TODO: To get the nucleo id, we need to follow nucleo_url

            #yield scrapy.Request(nucleo_url, callback=self.parse_nucleo_url)

    
    
    def parse_nucleo_url(self, response)
        pass


