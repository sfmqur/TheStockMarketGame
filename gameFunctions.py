import os


# str -> float
def getQuote(symbol):
    if os.name == 'Linux':
        os.system('python3 -m scrapy crawl getQuote -a symbol=\"%s\"' % symbol)
    elif os.name == 'nt':
        os.system('python -m scrapy crawl getQuote -a symbol=\"%s\"' % symbol)
    else:
        os.system('python -m scrapy crawl getQuote -a symbol=\"%s\"' % symbol)

    file = open('quote.txt', 'r')
    for l in file:
        quote = l
    file.close()
    os.system('rm quote.txt')
    return float(quote.strip())


# str -> dict of array[int:quantity, float:buy quote, float:current quote, float:percent change]
def loadPortfolio(user):
    if os.path.exists('data/%s-portfolio.txt' % user):
        file = open('data/%s-portfolio.txt' % user, 'r')
        portfolio = {}
        for l in file:
            entry = l.strip().split()
            portfolio[entry[0]] = [int(entry[1]), float(entry[2]), float(entry[3]), float(entry[4])]
        file.close()
        return portfolio
    else:
        return {}


# str, dict of arr[int, float, float, float]
def setPortfolio(user, port):
    file = open('data/%s-portfolio.txt' % user, 'w')
    for stock in port.keys():
        file.write('%s %s %s %s %s\n' %( stock, str(port[stock][0]), str(port[stock][1]),str(port[stock][2]),str(port[stock][3]) ))
    file.close()


# str -> void
def showPortfolio(user):
    port = loadPortfolio(user)
    print('Symbol:\t\t\tShares:\t\t\tThen::\t\t\ttNow:\t\t\tPercent Change:')
    for stock in port.keys():
        print("%s\t\t\t\t%g\t\t\t\t%g\t\t\t\t%g\t\t\t\t%g" % (stock, port[stock][0], port[stock][1], port[stock][2], port[stock][3]))


# str -> void
def refreshPortfolio(user):
    if os.path.exists('data/%s-portfolio.txt' % user):
        file = open('data/%s-portfolio.txt' % user, 'r')
        portfolio = {}
        for l in file:
            entry = l.strip().split()
            portfolio[entry[0]] = [int(entry[1]), float(entry[2])]
            portfolio[entry[0]].append(getQuote(entry[0]))
            portfolio[entry[0]].append(100 * (portfolio[entry[0]][2] - portfolio[entry[0]][1])/portfolio[entry[0]][1] )
        file.close()
        setPortfolio(user, portfolio)


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


def setHistory(user, newHistory):
    file = open('data/%s-history.txt' % user, 'w')
    for e in newHistory:
        file.write('%s %s %s %s %s\n' % (e[0].upper(), str(e[1]), str(e[2]), str(e[3]), str(e[4])))
    file.close()


# str -> void
def showHistory(user):
    history = loadHistory(user)
    bought = 0
    sold = 0
    print('Symbol:\t\t\tShares:\t\t\tPrice:\t\t\tBought:\t\t\tSold:')
    if history:
        for e in history:
            print("%s\t\t\t\t%g\t\t\t\t%g\t\t\t\t%g\t\t\t\t%g" % (e[0], e[1], e[2], e[3], e[4]))
            bought += e[3]
            sold += e[4]
        percent_change = (sold - bought)/bought * 100
        print("Net Values:")
        print('$%g bought\t$%g sold\t%g %%' % (bought, sold, percent_change))


# str, str, int -> void
def buyStock(user, symbol, quantity):
    quote = getQuote(symbol.upper())
    portfolio = loadPortfolio(user)
    history = loadHistory(user)
    balance = getBalance(user)
    symbol = symbol.upper()

    if quote * quantity <= balance:
        setBalance(user, balance - quote * quantity)
        if symbol in portfolio.keys():
            totalCost = portfolio[symbol][0] * portfolio[symbol][1]
            portfolio[symbol][0] += quantity
            totalCost += quote * quantity
            portfolio[symbol][1] = totalCost/portfolio[symbol][0]
            portfolio[symbol][2] = quote
            portfolio[symbol][3] = 100 * (portfolio[symbol][2] - portfolio[symbol][1])/portfolio[symbol][1]
            history.append([symbol, quantity, quote, quote*quantity, 0])
        else:
            portfolio[symbol] = [quantity, quote, quote, 0]
            history.append([symbol, quantity, quote, quote * quantity, 0])

        setPortfolio(user, portfolio)
        setHistory(user, history)

    else:
        print("you cannot afford that transaction")


# str, str, int -> void
# TODO: can sell stock that I do not have
# TODO: need to restructure with new set functions and portfolio as dictionary
def sellStock(user, symbol, quantity):
    quote = getQuote(symbol.upper())
    portfolio = loadPortfolio(user)
    history = loadHistory(user)
    symbol = symbol.upper()

    if symbol in portfolio.keys():
        if portfolio[symbol][0] >= quantity:
            portfolio[symbol][0] -= quantity
            history.append([symbol, quantity, quote, 0, quote * quantity])

            portfolio[symbol][2] = quote
            portfolio[symbol][3] = 100 * (portfolio[symbol][2] - portfolio[symbol][1]) / portfolio[symbol][1]

            setPortfolio(user, portfolio)
            setHistory(user, history)
    else:
        print("\nYou do not have enough %s stock to sell." %symbol)


# str -> [float: cash on hand, float: money added, float: account value]
def getBalance(user):
    balance = 0
    if os.path.exists('data/%s-account.txt' % user):
        file = open('data/%s-account.txt' % user, 'r')
        entry = file.readline().strip().split()
        balance = [float(entry[0]), float(entry[1]), float(entry[2])]
        file.close()
    return balance


# str , float -> void
def setBalance(user, newBalance):
    file = open('data/%s-account.txt' % user, 'w')
    file.write("%g %g %g" %(round(newBalance[0],2), round(newBalance[1],2), round(newBalance[2],2)))
    file.close()


# TODO: have wallet keep track of amount added to account and vs account value. and percent change of that
# maybe add this output to the end of show portfolio
# str -> void
def account(user):
    balance = getBalance(user)

    while True:
        command = input("You have a cash balance of $%g \n"
                        "You have invested %g and now you have an account value of %g at  %g%% change\n"
                        "Would you like to add, remove, update, or exit?\n"
                        % (balance[0], balance[1], balance[2], percentChange(balance[2], balance[1]))).strip()
        if command == "add":
            # TODO: idiot proofing
            add = float(input("How much would you like to add to your account?\n").strip())
            balance[0] += add
            balance[1] += add
        elif command == "remove":
            add = float(input("How much would you like to remove from your account?\n").strip())
            if add <= balance:
                balance[0] -= add
                balance[1] -= add
            else:
                print("You do not have that much money in your account.")
        elif command == 'update':
            refreshPortfolio(user)
            portfolio = loadPortfolio(user)
            value = balance[0]
            for stock in portfolio:
                value += portfolio[stock][0] * portfolio[stock][2]
            balance[2] = value
        elif command == "exit":
            setBalance(user, balance)
            break


# float, float -> float
def percentChange(val1, val2):
    return round(100* (val2-val1)/val1, 2)
