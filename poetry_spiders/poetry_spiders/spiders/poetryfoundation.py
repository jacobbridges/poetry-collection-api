# -*- coding: utf-8 -*-
import re
import scrapy
from math import ceil
from HTMLParser import HTMLParser
from poetry_spiders.items import PoemItem

h = HTMLParser()
subject_rgx = re.compile(r'#subject=[\d]+">(.+)<')
region_rgx = re.compile(r'#poet-region=[\d]+">(.+)<')
terms_rgx = re.compile(r'#poetic-terms=[\d]+">(.+)<')
period_rgx = re.compile(r'#school-period=[\d]+">(.+)<')

def clean_html(s):
	s = s.strip()
	s = h.unescape(s)
	s = ' '.join(s.split())
	return s

def get_start_urls(num_poems):
	urls = []
	for i in xrange(int(ceil(num_poems / 20.0))):
		urls.append('http://www.poetryfoundation.org/searchresults?page={}'.format(i+1))
	return tuple(urls)

def new_poem():
	item = PoemItem()
	item['title'] = ''
	item['keywords'] = ''
	item['text'] = ''
	item['region'] = ''
	item['author'] = ''
	item['year'] = ''
	item['period'] = ''
	item['classification'] = ''
	item['reference'] = ''
	return item


class PoetryfoundationSpider(scrapy.Spider):
    name = "poetryfoundation"
    allowed_domains = ["poetryfoundation.org"]
    start_urls = get_start_urls(12994)

    def parse(self, response):
        for href in response.css("a.title::attr('href')"):
        	url = response.urljoin(href.extract())
        	yield scrapy.Request(url, callback=self.parse_poem_page)

    def parse_poem_page(self, response):
    	item = new_poem()
    	item['title'] = clean_html(response.css('#poem-top > h1').xpath('text()').extract()[0])
    	item['author'] = response.css('#poemwrapper .author a').xpath('text()').extract()
    	if item['author']:
    		item['author'] = clean_html(item['author'][0])
    	else:
    		item['author'] = response.css('#poemwrapper .author').xpath('text()').extract()
    		if item['author']:
    			item['author'] = item['author'][0].split('By')[1:]
    			item['author'] = ''.join(item['author'])
    			item['author'] = clean_html(item['author'])
    		else:
    			item['author'] = 'Unkown'
    	item['text'] = response.css('#poem .poem div').xpath('text()').extract()
    	if item['text']:
    		item['text'] = list(map(lambda x: clean_html(x), item['text']))
    		item['text'] = list(filter(lambda x: bool(x), item['text']))
    	item['keywords'] = []
    	for a in response.css('.about .section a').extract():
    		match = subject_rgx.search(a)
    		if match:
    			matches = h.unescape(match.groups()[0]).split('&')
    			matches = list(map(lambda x: x.strip(), matches))
    			item['keywords'] = item['keywords'] + matches
    			continue
    		match = region_rgx.search(a)
    		if match:
    			item['region'] = clean_html(match.groups()[0])
    			continue
    		match = terms_rgx.search(a)
    		if match:
    			item['classification'] = clean_html(match.groups()[0])
    			continue
    		match = period_rgx.search(a)
    		if match:
    			item['period'] = clean_html(match.groups()[0])
    			continue
    	list(map(lambda x: clean_html(x), item['keywords']))
    	item['keywords'] = list(filter(lambda x: bool(x), item['keywords']))
    	item['reference'] = response.url

    	yield item