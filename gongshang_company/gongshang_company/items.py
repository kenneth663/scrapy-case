# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from .models.es_types import CompanyType

from elasticsearch_dsl.connections import connections
es = connections.create_connection(CompanyType._doc_type.using)

class HuijuCompanyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class CompanyItem(scrapy.Item):

    company_name = scrapy.Field()   #公司名称
    legal_person = scrapy.Field()   #法人
    registered_capital = scrapy.Field()    #注册资本
    telephone_number = scrapy.Field()   #电话
    email = scrapy.Field()  #邮箱
    company_url = scrapy.Field()    #公司网址
    address = scrapy.Field()    #地址
    registration_time = scrapy.Field()  #注册时间
    company_state = scrapy.Field()  #公司状态
    latest_update_time = scrapy.Field() #最新更新时间
    registration_number = scrapy.Field()    #工商注册号
    organization_code = scrapy.Field()  #组织机构代码
    uniform_credit_code = scrapy.Field()    #统一信用代码
    company_type = scrapy.Field()   #公司类型
    taxpayer_number = scrapy.Field()    #纳税人识别号
    industry = scrapy.Field()   #行业
    business_term = scrapy.Field()  #营业期限
    approval_date = scrapy.Field()  #核准日期
    registration_authority = scrapy.Field() #登记机关
    english_name = scrapy.Field()   #英文名称
    registered_address = scrapy.Field() #注册地址
    operation_scope = scrapy.Field()    #经营范围

    def save_to_es(self):
        company = CompanyType()
        company.company_name = self["company_name"]
        company.legal_person = self["legal_person"]
        company.registered_capital = self["registered_capital"]
        company.telephone_number = self["telephone_number"]
        company.email = self["email"]
        company.company_url = self["company_url"]
        company.address = self["address"]
        company.registration_time = self["registration_time"]
        company.company_state = self["company_state"]
        company.latest_update_time = self["latest_update_time"]
        company.registration_number = self["registration_number"]
        company.organization_code = self["organization_code"]
        company.uniform_credit_code = self["uniform_credit_code"]
        company.company_type = self["company_type"]
        company.taxpayer_number = self["taxpayer_number"]
        company.industry = self["industry"]
        company.business_term = self["business_term"]
        company.approval_date = self["approval_date"]
        company.registration_authority = self["registration_authority"]
        company.english_name = self["english_name"]
        company.registered_address = self["registered_address"]
        company.operation_scope = self["operation_scope"]

        company.save()

        return





