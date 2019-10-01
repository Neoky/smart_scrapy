import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import pandas as pd
from dragnet import extract_content, extract_content_and_comments
from dragnet.util import load_pickled_model
import nltk
nltk.download('stopwords')
nltk.download('punkt')

content_extractor = load_pickled_model(
    'kohlschuetter_readability_weninger_content_model.pkl.gz')
content_comments_extractor = load_pickled_model(
    'kohlschuetter_readability_weninger_comments_content_model.pkl.gz')

class SmartSpider(CrawlSpider):
    name = "Smart"
    allowed_domains = ['pbs.org', 'www.pbs.org']
    custom_settings = {
        'DEPTH_LIMIT': 1
    }
    start_urls = [
        'https://www.pbs.org/newshour/',
    ]

    def __init__(self):
        self.columns = ["summary", "content", "comments", "url"]
        #self.pd = pd.DataFrame(columns=self.columns)
        #if pd.read_csv("scrapy.csv"):
        #    self.pd = pd.read_csv("scrapy.csv")
        #else:
        #    self.pd = pd.DataFrame(columns=self.columns)

    #def start_requests(self):
    #    for url in urls:
    #        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for href in response.xpath('//a/@href').getall():
            yield scrapy.Request(response.urljoin(href), self.parse)
        # get main article without comments
        #for next_page in response.css('a::attr(href)').extract_first():
        #    if next_page is not None:
        #        next_page = response.urljoin(next_page)
        #        yield scrapy.Request(next_page, callback=self.parse)

        content = content_extractor.extract(response.body, encoding='utf-8')
        content_comments = content_comments_extractor.extract(response.body, encoding='utf-8')

        row = [(summary, content, content_comments, response.url)]
        df = pd.DataFrame(data=row, columns=self.columns)
        #self.pd.append(row)
        df.to_csv("scrapy.csv", mode="a")

        yield {
            'content': content_extractor.extract(response.body),
            'comments': content_comments_extractor.extract(response.body),
            'url': response.url,
        }
        #page = response.url.split("/")[-2]
        #filename = 'quotes-%s.html' % page
        #with open(filename, 'wb') as f:
        #    f.write(response.body)
        #self.log('Saved file %s' % filename)