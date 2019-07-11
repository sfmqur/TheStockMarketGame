import scrapy


# TODO: the code here is a template copied from the tutorial
# the spider needs to ask which stock symbol to crawl, and then crawl that stocks page
# it would be nice to return a number value of the current price. I need to make my main program communicate
# with this one
# a hack might be to write the symbol into a temp file, then import it here. then delete the file.
class QuoteSpider(scrapy.Spider):
    name = "getQuote"

    stock = 'AMD'
    start_urls = ["https://www.barchart.com/stocks/quotes/%s/overview" % stock]

    def parse(self, response):
        filename = 'quote-%s.html' % stock
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
