import scrapy


# TODO: the code here is a template copied from the tutorial
# the spider needs to ask which stock symbol to crawl, and then crawl that stocks page
# it would be nice to return a number value of the current price. I need to make my main program communicate
# with this one
# a hack might be to write the symbol into a temp file, then import it here. then delete the file.
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
