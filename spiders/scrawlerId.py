# coding=utf-8
import urllib

import scrapy


class CompanyIdSpider(scrapy.Spider):
    name = "scrawlerId"
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
            yield scrapy.Request(href_item.extract(), self.parse_info_page)

    def parse_info_page(self, response):
        for title in response.css("ul.company_list div.company_list_text"):
            print "company href: %s" % title.css("a::attr(href)").extract_first()
            yield scrapy.Request(title.css("a::attr(href)").extract_first(), self.parse_id)

        for next in response.css("ul.m_page a.next"):
            next_url = next.css("a::attr(href)").extract_first()
            if not next_url == '#':
                next_url = "http://china.99114.com/" + next_url
                print "next url: %s" % next_url
                yield scrapy.Request(next_url, self.parse_info_page)

    def parse_id(self, response):
        print "company name: %s" % response.css("div.xq_gsxx span.addR")[0].css("a::text").extract_first()
        print "company location: %s" % response.css("div.xq_gsxx span.addR")[2].css("span::text").extract_first()
        print "company id: %s" % response.css("div.xq_gsxx span.addR")[6].css("span::text").extract_first()
        print "company tel: %s" % response.css("div.xq_lxfs span.addR")[1].css("span::text").extract_first()
        yield {
            "id": response.css("div.xq_gsxx span.addR")[6].css("span::text").extract_first()
        }
