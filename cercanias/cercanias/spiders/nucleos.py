# -*- coding: utf-8 -*-
import scrapy
from cercanias.items import NucleosItem
import re


class NucleosSpider(scrapy.Spider):
    name = "nucleos"
    allowed_domains = ["renfe.com"]
    start_urls = (
        'http://www.renfe.com/viajeros/cercanias/',
    )

    def __init__(self, mongodb_uri='', mongodb_name=''):
        self.mongodb_uri = mongodb_uri
        self.mongodb_name = mongodb_name

    def parse(self, response):

        # Get nucleos by columns
        for nucleo_div in response.xpath('//div[@id="colB"]/div[@class="colB1" or @class="colB2" or @class="colB3"]'):

            # Get nucleo name
            nucleo_name_array = nucleo_div.xpath('h3/a/@title').extract()
            if not nucleo_name_array or not isinstance(nucleo_name_array, list) or len(nucleo_name_array) <= 0:
                continue

            nucleo_name = nucleo_name_array[0]

            # Get link to image
            nucleo_img_array = nucleo_div.xpath('p/a/img/@src').extract()
            if not nucleo_img_array or not isinstance(nucleo_img_array, list) or len(nucleo_img_array) <= 0:
                continue

            nucleo_img_link = nucleo_img_array[0]

            # Dirty hack!
            nucleo_img_link = nucleo_img_link.replace('../..', 'http://www.renfe.com')

            # Build the item to send it to callback
            item = NucleosItem()

            item['nucleo_name'] = nucleo_name
            item['nucleo_img_link'] = nucleo_img_link


            # Get link to nucleo page
            nucleo_link_array = nucleo_div.xpath('h3/a/@href').extract()
            if not nucleo_link_array or not isinstance(nucleo_link_array, list) or len(nucleo_link_array) <= 0:
                continue

            nucleo_link = response.urljoin(nucleo_link_array[0])

            # Load the page pointed by the link using a callback
            request = scrapy.Request(nucleo_link, callback = self.parse_nucleo_url)

            # Pass addditional arguments to callback
            request.meta['item'] = item

            yield request



    def parse_nucleo_url(self, response):
        item = response.meta['item']

        nucleo_iframe = response.xpath('//iframe[@class="marco"]')

        nucleo_id_array = nucleo_iframe.xpath('@src').extract()
        if not nucleo_id_array or not isinstance(nucleo_id_array, list) or len(nucleo_id_array) <= 0:
            yield None

        iframe_url = nucleo_id_array[0]

        # Extract nucleo id from iframe url using regex
        try:
            value_regex = re.compile("(?<=NUCLEO=)(?P<value>.*?)(?=&)")
            m = value_regex.search(iframe_url)
            nucleo_id = m.group('value')
        except Exception:
            nucleo_id = ""

        item['nucleo_id'] = nucleo_id

        # Parse nucleo stations from url
        request = scrapy.Request(iframe_url, callback=self.parse_nucleo_stations)

        request.meta['item'] = item

        yield request


    def parse_nucleo_stations(self, response):
        item = response.meta['item']

        nucleo_stations_select = response.xpath('//div[@id="contenedor"]/h1/select[@name="o"]')

        nucleo_stations_array = nucleo_stations_select.xpath('option')
        if not nucleo_stations_array or not isinstance(nucleo_stations_array, list) or len(nucleo_stations_array) <= 0:
            yield None

        nucleo_stations = nucleo_stations_array[0]

        stations = []
        for n_array in nucleo_stations_array:
            n_stations = n_array.xpath('text()').extract()

            if not n_stations or not isinstance(n_stations, list) or len(n_stations) <= 0:
                continue

            stations.append(n_stations[0].strip().encode('utf8'))

        item['nucleo_stations'] = stations

        yield item

