import os


# str -> float
def getQuote(symbol):
    os.system('python3 -m scrapy crawl getQuote -a symbol=\"%s\"' % symbol)
    file = open('quote.txt', 'r')
    for l in file:
        quote = l
    file.close()
    os.system('rm quote.txt')
    return float(quote.strip())

# str, str, int -> void
def buyStock(user, symbol, quantity):
    print('buying stock')


# str, str, int -> void
def sellStock(user, symbol, quantity):
    print('selling stock')


# str -> void
def showPortfolio(user):
    if os.path.exists('data/%s-portfolio.txt' % user):
        file = open('data/%s-portfolio.txt' % user, 'r')
        print('Symbol:\tShares:\tPurchase Value:\tCurrent Value')

        file.close()
    else:
        print('you do not own any stock')


# str -> void
def showHistory(user):
    print('this is your history')
    print('B/S:\tDatestamp:\tSymbol:\tQuantity:\tShare Price:\tTotal')
