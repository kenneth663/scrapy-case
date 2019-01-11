# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
try:
    from urllib import parse
except:
    import urlparse as parse
from huiju_company.items import CompanyItem


class CompanyspiderSpider(scrapy.Spider):

    def __init__(self, pg_s=1, *args, **kwargs):
        super(CompanyspiderSpider, self).__init__(*args, **kwargs)
        self.pg_s = int(pg_s)

    name = 'companyspider'
    allowed_domains = ['.com']
    city_dict = {'anhui':('https://.html', 145207),
                 'beijing': ('https://.html', 100),
                 'chongqing': ('https://.html', 100),
                 'fujian': ('https://.html', 100),
                 'guangdong': ('https://.html', 100),
                 'guangxi': ('https://.html', 100),
                 'gansu': ('https://.html', 100),
                 'guizhou': ('https://.html', 100),
                 'hebei': ('https://.html', 100),
                 'henan': ('https://.html', 100),
                 'hainan': ('https://.html', 100),
                 'hubei': ('https://.html', 100),
                 'hunan': ('https://.html', 100),
                 'heilongjiang': ('https://.html', 100),
                 'jilin': ('https://.html', 100),
                 'jiangsu': ('https://.html', 100),
                 'jiangxi': ('https://.html', 100),
                 'liaoning': ('https://.html', 100),
                 'neimenggu': ('https://.html', 100),
                 'ningxia': ('https://.html', 100),
                 'qinghai': ('https://.html', 100),
                 'shanghai': ('https://.html', 100),
                 'sichuan': ('https://.html', 100),
                 'shandong': ('https://.html', 100),
                 'shanxi': ('https://.html', 100),
                 'shanxi2': ('https://.html', 100),
                 'tianjin': ('https://.html', 100),
                 'xinjiang': ('https://.html', 100),
                 'xizang': ('https://.html', 100),
                 'yunnan': ('https://.html', 100),
                 'zhejiang': ('https://.html', 100),
                 }
    city = "anhui"
    start_urls = [city_dict[city][0]]

    def parse(self, response):

        # 获取当前页码
        current_page_num_str = response.xpath('//div[@class="resultList"]/ul/a[last()-1]/@data-pn').extract_first()
        try:
            current_page_num = int(current_page_num_str)
        except:
            current_page_num = 1
        # 若当前页码小于起始页码，直接从起始页开始爬取
        if current_page_num < 5:
            next_url = self.start_urls[0] + "?pn={}".format(5)
            yield Request(url=next_url, callback=self.parse)

        # 解析列表页中所有url并交给解析
        post_urls = response.xpath('//div[@class="choosedResultbox companyList"]/div[2]/div/div/a/@href').extract()
        for post_url in post_urls:
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse_detail)

        # 若当前页码小于最大页码，则继续将下一页交给scrapy下载
        if current_page_num < self.city_dict[self.city][1]:
            next_url = self.city_dict[self.city][0] + "?pn={}".format(current_page_num+1)
            yield Request(url=next_url, callback=self.parse)

        #
        # urls = response.xpath('//div[@class="company-name"]/a[@class="linkBtn inline-block ellipsis"]/@href').extract()
        # for url in urls:
        #     yield Request(url=response.urljoin(url), callback=self.parse_detail)
        # next_page_status = response.css('.pagination a::attr(href)').extract()
        # if next_page_status != '':
        #     page = response.css('.pagination a::attr(href)').extract()
        #     next_page = response.urljoin(page[-2])
        #     yield Request(url=next_page, callback=self.parse_detail)




    def parse_detail(self, response):
        city_item = CompanyItem()
        # 提取文章的具体字段
        company_name = response.xpath('//div[@class="company-info clear"]/div[2]/div/div/a/h1/text()').extract_first()  #公司名称
        legal_person = response.xpath('//div[@class="text-info"]/div[2]/div[1]/div[1]/span/text()').extract_first() #法人
        registered_capital = response.xpath('//div[@class="text-info"]/div[2]/div[1]/div[2]/span/text()').extract_first()   #注册资本
        telephone_number = response.xpath('//div[@class="text-info"]/div[2]/div[2]/div/div/span[1]/text()').extract_first() #电话
        email = response.xpath('//div[@class="text-info"]/div[2]/div[2]/div[2]/span/text()').extract_first()    #邮箱
        company_url = response.xpath('//div[@class="text-info"]/div[2]/div[2]/div[3]/span/a/text()').extract_first()    #公司网址
        address = response.xpath('//div[@class="text-info"]/div[2]/div[3]/div/span/text()').extract_first() #地址
        registration_time = response.xpath('//table[@class="gsxx-tb-01"]/tr/td[3]/p[2]/text()').extract_first() #注册时间
        company_state = response.xpath('//table[@class="gsxx-tb-01"]/tr/td[4]/p[2]/text()').extract_first() #   公司状态
        latest_update_time = response.xpath('//table[@class="gsxx-tb-01"]/tr/td[5]/p[3]/text()').extract_first()    #最新更新时间
        registration_number = response.xpath('//table[@class="gsxx-tb-02"]/tr[1]/td[2]/text()').extract_first()   #工商注册号
        organization_code = response.xpath('//table[@class="gsxx-tb-02"]/tr[1]/td[4]/text()').extract_first()   #组织代码机构
        uniform_credit_code = response.xpath('//table[@class="gsxx-tb-02"]/tr[2]/td[2]/text()').extract_first() #统一信用编码
        company_type = response.xpath('//table[@class="gsxx-tb-02"]/tr[2]/td[4]/text()').extract_first()    #公司类型
        taxpayer_number = response.xpath('//table[@class="gsxx-tb-02"]/tr[3]/td[2]/text()').extract_first() #纳税人识别号
        industry = response.xpath('//table[@class="gsxx-tb-02"]/tr[3]/td[4]/a/text()').extract_first()  #行业
        business_term = response.xpath('//table[@class="gsxx-tb-02"]/tr[4]/td[2]/text()').extract_first()   #营业期限
        approval_date = response.xpath('//table[@class="gsxx-tb-02"]/tr[4]/td[4]/text()').extract_first()   #核准日期
        registration_authority = response.xpath('//table[@class="gsxx-tb-02"]/tr[5]/td[2]/text()').extract_first()  #登记机关
        english_name = response.xpath('//table[@class="gsxx-tb-02"]/tr[5]/td[4]/text()').extract_first()    #英文名称
        registered_address = response.xpath('//table[@class="gsxx-tb-02"]/tr[6]/td[2]/text()').extract_first()  #注册地址
        operation_scope = response.xpath('//table[@class="gsxx-tb-02"]/tr[7]/td[2]/div/text()').extract_first() #经营范围

        city_item["company_name"] = company_name
        city_item["legal_person"] = legal_person
        city_item["registered_capital"] = registered_capital
        city_item["telephone_number"] = telephone_number
        city_item["email"] = email
        city_item["company_url"] = company_url
        city_item["address"] = address
        city_item["registration_time"] = registration_time
        city_item["company_state"] = company_state
        city_item["latest_update_time"] = latest_update_time
        city_item["registration_number"] = registration_number
        city_item["organization_code"] = organization_code
        city_item["uniform_credit_code"] = uniform_credit_code
        city_item["company_type"] = company_type
        city_item["taxpayer_number"] = taxpayer_number
        city_item["industry"] = industry
        city_item["business_term"] = business_term
        city_item["approval_date"] = approval_date
        city_item["registration_authority"] = registration_authority
        city_item["english_name"] = english_name
        city_item["registered_address"] = registered_address
        city_item["operation_scope"] = operation_scope

        yield city_item