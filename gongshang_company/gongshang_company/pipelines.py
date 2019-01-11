# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
from .models.es_types import CompanyType
from twisted.enterprise import adbapi
import json
import os
import csv

class HuijuCompanyPipeline(object):
    def process_item(self, item, spider):
        return item

class ElasticsearchPipeline(object):
    #将数据写入到es中
    def process_item(self, item, spider):
        #将item转换为es的数据
        item.save_to_es()

        return item

class JsonWithEncodingPipeline(object):
    #自定义json文件导出
    def __init__(self):
        self.file = codecs.open('company.json', 'w', encoding="utf-8")
    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item
    def spider_closed(self, spider):
        self.file.close()







