import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.request import referer_str
import nltk

class MySpider(CrawlSpider):
    name = 'startup'
    allowed_domains = ['techcrunch.com', 'startupsavant.com', 'tech.co','techstartups.com', 'entrepreneur.com', 'wired.com', 'crunchbase.com', 'mashable.com']
    
    start_urls = ['https://techstartups.com/category/tech-startups/page/53/', 'https://techstartups.com/category/tech-startups/page/57/', 'https://techstartups.com/category/tech-startups/page/63/', 'https://techstartups.com/category/tech-startups/page/67/', 'https://techstartups.com/category/tech-startups/page/73/', 'https://techstartups.com/category/tech-startups/page/77/', 'https://techstartups.com/category/tech-startups/page/83/', 'https://techstartups.com/category/tech-startups/page/87/', 'https://techstartups.com/category/tech-startups/page/93/', 'https://techstartups.com/category/tech-startups/page/97/', 'https://techstartups.com/category/tech-startups/page/203/', 'https://techstartups.com/category/tech-startups/page/207/', 'https://techcrunch.com/startups/page/205/', 'https://techcrunch.com/startups/page/210/', 'https://techcrunch.com/startups/page/215/', 'https://techcrunch.com/startups/page/220/', 'https://techcrunch.com/startups/page/225/', 'https://techcrunch.com/startups/page/230/', 'https://techcrunch.com/startups/page/235/','https://techcrunch.com/startups/page/240/', 'https://techcrunch.com/startups/page/245/', 'https://techcrunch.com/startups/page/250/', 'https://techcrunch.com/startups/page/255/', 'https://techcrunch.com/startups/page/260/', 'https://techcrunch.com/startups/page/265/', 'https://techcrunch.com/startups/page/270/', 'https://techcrunch.com/startups/page/275/', 'https://techcrunch.com/startups/page/280/', 'https://techcrunch.com/startups/page/285/', 'https://techcrunch.com/startups/page/290/', 'https://techcrunch.com/startups/page/295/', 'https://techcrunch.com/startups/page/300/']  
    
    
    custom_settings = {
        'DEPTH_LIMIT': '4',
        'DOWNLOAD_DELAY': '.2',
        'CONCURRENT_ITEMS': '300'
        
    }
    
    #Rules
    rules = [Rule(LinkExtractor(unique=True), callback='parse', follow=True)]
    
	#The info that I want and yield it
    def parse(self, response):
    	
    	Text = ''
		
		#techcrunch	
    	if 'https://techcrunch.com/2' in response.url:
    		Title = response.css('h1.article__title::text').get()

    		for node in response.xpath('//div[@class="article-content"]//p'):
    			Text = ''.join(node.xpath('string()').extract())
    			
    		#Checks for null vals
    		if referer_str(response.request) != '' or Title != '' or Text != ''  or Text != ' ' or Text.encode('utf-8') != "b''" or Text != 'None' or Title != 'None': 
    			yield {
    				'SourceLink': referer_str(response.request),
    				'Link': response.url,
    				'Title': str(Title).encode('utf-8'),
    				'Text': str(Title).encode('utf-8') + str(Text).encode('utf-8'),
    				}
    	#startupsavant
    	elif 'https://startupsavant.com/news' in response.url:
    		Title = response.css('h1.headline::text').get()
    		
    		for node in response.xpath('//div[@class="row"]//p'):
    			Text = ''.join(node.xpath('string()').extract())
    		
    		#Checks for null vals
    		if referer_str(response.request) != '' or Title != '' or Text != '' or Text != ' ' or Text.encode('utf-8') != "b''" or Text != 'None' or Title != 'None':
    			yield {
    				'SourceLink': referer_str(response.request),
    				'Link': response.url,
    				'Title': str(Title).encode('utf-8'),
    				'Text': str(Title).encode('utf-8') + str(Text).encode('utf-8'),
    				}
    				
    	#techstartups
    	elif 'https://techstartups.com/2' in response.url:
    		Title = response.css('div.post_header_title h1::text').get()
    		
    		for node in response.xpath('//div[@class="post_content_wrapper"]//p'):
    			Text = ''.join(node.xpath('string()').extract())
    		
    		#Checks for null vals
    		if referer_str(response.request) != '' or Title != '' or Text != '' or Text != ' ' or Text.encode('utf-8') != "b''" or Text != 'None' or Title != 'None':
    			yield {
    				'SourceLink': referer_str(response.request),
    				'Link': response.url,
    				'Title': str(Title).encode('utf-8'),
    				'Text': str(Title).encode('utf-8') + str(Text).encode('utf-8'),
    				}

