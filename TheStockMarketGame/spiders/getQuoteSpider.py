import scrapy


class QuoteSpider(scrapy.Spider):
    name = "getQuote"

    def __init__(self, symbol=''):
        self.stock = symbol
        self.start_urls = ["https://finance.yahoo.com/quote/%s" % symbol]

    def parse(self, response):
        quote = response.xpath('//span[@data-reactid="14"]/text()').get()
        file = open('quote.txt', 'w')
        file.write(quote)
        file.close()
        self.log('%s %s' % (self.symbol, quote))
