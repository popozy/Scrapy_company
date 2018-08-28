# coding=utf-8
import urllib

import scrapy


class CompanySpider(scrapy.Spider):
    name = "scrawlerChina"
    start_urls = [
        "http://china.99114.com/",
    ]

    def parse(self, response):
        for href_item in response.css("div.left_qghy a::attr(href)"):
                print "city href: %s " % href_item.extract()
                yield scrapy.Request(href_item.extract(), self.parse_serial)

    def parse_serial(self, response):
        for href_item in response.css("div.left_qyhy a::attr(href)"):
            print "company serial href: %s" % href_item.extract()
            yield scrapy.Request(href_item.extract(), self.parse_company)

    def parse_company(self, response):
        for title in response.css("ul.company_list div.company_list_text"):
            print "company name: %s" % title.css("a::text").extract_first()
            yield {
                "company": title.css("a::text").extract_first()
            }

        for next in response.css("ul.m_page a.next"):
            next_url = next.css("a::href").extract_first()
            if not next_url == '#':
                next_url = "http://china.99114.com/" + next_url
                print "next url: %s" % next_url
                yield scrapy.Request(next_url, self.parse_company)

        # for title in response.css("div.g"):
        #     yield {
        #         "text": str(title.css("h3.r a::text").extract_first()) + str(title.css("h3.r a b::text").extract_first())
        #     }
        #
        # next_url = "https://www.google.com" + response.css("td.b a::attr(href)").extract()[1]
        # print "nexturl:" + response.css("td.b a::attr(href)").extract()[1]
        # next_response = response.replace(url=next_url)
        # if next_response is not None:
        #     yield scrapy.Request(next_response.url, callback=self.parse)
