# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlHustItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Ma_HP = scrapy.Field()
    Ten_HP = scrapy.Field()
    Thoi_luong = scrapy.Field()
    So_tin_chi = scrapy.Field()
    TC_hoc_phi = scrapy.Field()
    Trong_so = scrapy.Field()
    pass
