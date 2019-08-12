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


# str -> 2darr[str, int, float]
def loadPortfolio(user):
    if os.path.exists('data/%s-portfolio.txt' % user):
        file = open('data/%s-portfolio.txt' % user, 'r')
        portfolio = []
        for l in file:
            entry = l.strip().split()
            portfolio.append(entry)
        file.close()
        for e in portfolio:
            e[1] = int(e[1])
            e[2] = float(e[2])
        return portfolio
    else:
        return []


# str -> 2darr[str, int, float, float, float]
def loadHistory(user):
    if os.path.exists('data/%s-history.txt' % user):
        file = open('data/%s-history.txt' % user, 'r')
        history = []
        for l in file:
            entry = l.strip().split()
            history.append(entry)
        file.close()
        for e in history:
            e[1] = int(e[1])
            e[2] = float(e[2])
            e[3] = float(e[3])
            e[4] = float(e[4])
        return history
    else:
        return []


# str, str, int -> void
def buyStock(user, symbol, quantity):
    quote = getQuote(symbol.upper())
    portfolio = loadPortfolio(user)
    history = loadHistory(user)

    for i in range(len(portfolio)):
        if symbol.upper() == portfolio[i][0]:
            portfolio[i][1] += quantity
            portfolio[i][2] += quote * quantity
            history.append([symbol, quantity, quote, quote * quantity, 0])
            break
        elif i == len(portfolio) - 1:
            portfolio.append([symbol, quantity, quantity * quote])
            history.append([symbol, quantity, quote, quote * quantity, 0])
    file = open('data/%s-portfolio.txt' % user, 'w')
    for e in portfolio:
        file.write('%s %s %s\n' %(e[0].upper(), str(e[1]), str(e[2]) ) )
    file.close()
    # modify history file
    file = open('data/%s-history.txt' % user, 'w')
    for e in history:
        file.write('%s %s %s %s %s\n' % (e[0].upper(), str(e[1]), str(e[2]), str(e[3]), str(e[4]) ) )
    file.close()


# str, str, int -> void
def sellStock(user, symbol, quantity):
    quote = getQuote(symbol.upper())
    portfolio = loadPortfolio(user)
    history = loadHistory(user)

    for i in range(len(portfolio)):
        if symbol.upper() == portfolio[i][0]:
            if quantity <= portfolio[i][1]:
                portfolio[i][1] -= quantity
                portfolio[i][2] -= quote * quantity
                history.append([symbol, quantity, quote, 0, quote * quantity])
                break
            else:
                print('You do not have enough shares to sell.')
                break
        elif i == len(portfolio) - 1:
            print('You do not have enough shares to sell.')
    file = open('data/%s-portfolio.txt' % user, 'w')
    for e in portfolio:
        file.write('%s %s %s\n' % (e[0].upper(), str(e[1]), str(e[2])))
    file.close()
    # modify history file
    file = open('data/%s-history.txt' % user, 'w')
    for e in history:
        file.write('%s %s %s %s %s\n' % (e[0].upper(), str(e[1]), str(e[2]), str(e[3]), str(e[4])))
    file.close()


# str -> void
def showPortfolio(user):
    if os.path.exists('data/%s-portfolio.txt' % user):
        file = open('data/%s-portfolio.txt' % user, 'r')
        portfolio = []
        purchase_value = 0
        current_value = 0
        for l in file:
            entry = l.strip().split()
            portfolio.append(entry)
        file.close()
        for e in portfolio:
            e[1] = int(e[1])
            e[2] = float(e[2])
            e.append(getQuote(e[0]) * e[1])
            e.append((e[3] - e[2])/e[2] * 100)
        print('Symbol:\t\tShares:\t\tThen::\t\tNow:\t\tPercent Change:')
        for e in portfolio:
            print("%s\t\t%g\t\t%g\t\t%g\t\t%g" % (e[0], e[1], e[2], e[3], e[4]))
            purchase_value += e[2]
            current_value += e[3]
        percent_change = (current_value - purchase_value)/purchase_value * 100
        print('\t\t%g\t\t%g\t\t%g' % (purchase_value, current_value, percent_change))

    else:
        print('you do not own any stock')


# str -> void
def showHistory(user):
    history = loadHistory(user)
    bought = 0
    sold = 0
    print('Symbol:\t\tShares:\t\tPrice:\t\tBought:\t\tSold:')
    for e in history:
        print("%s\t\t%g\t\t%g\t\t%g\t\t%g" % (e[0], e[1], e[2], e[3], e[4]))
        bought += e[3]
        sold += e[4]
    percent_change = (sold - bought)/bought * 100
    print('\t\t\t\t\t\t%g\t\t%g\t\t%g percent' % (bought, sold, percent_change))

