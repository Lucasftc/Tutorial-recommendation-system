# -*- coding: utf-8 -*-
from openpyxl import Workbook
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item

class TeacherPipeline(object):
    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(['姓名','基本信息','联系方式', '教育经历', '工作经历', '研究方向', '教授课程', '科研项目', '科研成果', '社会兼职', '培养要求', '荣誉获奖'])
        
    def process_item(self, item, spider):
        line = [item['name'],item['info'],item['contact'], item['education_experience'], item['work_experience'], item['direction'], item['lesson'], item['project'], item['result'], item['social_work'], item['requirement'], item['reputation']]
        self.ws.append(line)
        self.wb.save('teacher.xlsx')
        return item

class ArticlePipeline(object):
    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(['author', 'title', 'abstract', 'platform'])
    
    def process_item(self, item, spider):
        line = [item['author'], item['title'], item['abstract'], item['platform']]
        self.ws.append(line)
        self.wb.save('article.xlsx')
        return item