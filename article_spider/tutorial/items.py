# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class filedownloaditem(scrapy.Item):
    file_urls = scrapy.Field()
    files = scrapy.Field()

class teacheritem(scrapy.Item):
    name=scrapy.Field()
    info = scrapy.Field()
    contact = scrapy.Field()
    education_experience = scrapy.Field()
    work_experience = scrapy.Field()
    direction = scrapy.Field()
    lesson=scrapy.Field()
    project = scrapy.Field()
    result = scrapy.Field()
    social_work = scrapy.Field()
    reputation = scrapy.Field()
    requirement = scrapy.Field()
    
class articleitem(scrapy.Item):
    author = scrapy.Field()
    title = scrapy.Field()
    abstract = scrapy.Field()
    platform=scrapy.Field()

    
    
