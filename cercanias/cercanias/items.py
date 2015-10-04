# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NucleosItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    nucleo_id = scrapy.Field()
    nucleo_name = scrapy.Field()
    nucleo_img_link = scrapy.Field()
    nucleo_stations = scrapy.Field()
