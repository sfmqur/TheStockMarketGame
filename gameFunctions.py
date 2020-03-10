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


# TODO: turn portfolio into dictionary
# str -> 2darr[str, int, float]
def loadPortfolio(user):
    if os.path.exists('data/%s-portfolio.txt' % user):
        file = open('data/%s-portfolio.txt' % user, 'r')
        portfolio = {}
        for l in file:
            entry = l.strip().split()
            portfolio[entry[0]] = [int(entry[1]), float(entry[2])]
            portfolio[entry[0]].append(getQuote(entry[0]))
            portfolio[entry[0]].append(100 * (portfolio[entry[0]][2] - portfolio[entry[0]][1])/portfolio[entry[0]][1] )
        file.close()
        return portfolio
    else:
        return {}


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
    balance = getBalance(user)
    symbol = symbol.upper()

    if quote * quantity <= balance:
        setBalance(user, balance - quote * quantity)
        if symbol in portfolio.keys():
            totalCost = portfolio[symbol][0] * portfolio[symbol][1]
            portfolio[symbol][0] += quantity
            totalCost += quote * quantity
            portfolio[symbol][1] = totalCost/portfolio[symbol][0]
            history.append([symbol, quantity, quote, quote*quantity, 0])
        else:
            portfolio[symbol] = [quantity, quote]
            history.append([symbol, quantity, quote, quote * quantity, 0])

        setPortfolio(user, portfolio)
        setHistory(user, history)

    else:
        print("you cannot afford that transaction")


# str, str, int -> void
# TODO: can sell stock that I do not have
def sellStock(user, symbol, quantity):
    quote = getQuote(symbol.upper())
    portfolio = loadPortfolio(user)
    history = loadHistory(user)

    for i in range(len(portfolio)):
        if symbol.upper() == portfolio[i][0]:
            if quantity <= portfolio[i][1]:
                setBalance(user, getBalance(user) + quote * quantity)
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
    port = loadPortfolio(user)
    print('Symbol:\t\t\tShares:\t\t\tThen::\t\t\ttNow:\t\t\tPercent Change:')
    for stock in port.keys():
        print("%s\t\t\t\t%g\t\t\t\t%g\t\t\t\t%g\t\t\t\t%g" % (stock, port[stock][0], port[stock][1], port[stock][2], port[stock][3]))


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


# str -> float
def getBalance(user):
    balance = 0
    if os.path.exists('data/%s-wallet.txt' % user):
        file = open('data/%s-wallet.txt' % user, 'r')
        balance = float(file.readline().strip())
        file.close()
    return balance


# str , float -> void
def setBalance(user, newBalance):
    file = open('data/%s-wallet.txt' % user, 'w')
    file.write(str(newBalance))
    file.close()


def setHistory(user, newHistory):
    file = open('data/%s-history.txt' % user, 'w')
    for e in newHistory:
        file.write('%s %s %s %s %s\n' % (e[0].upper(), str(e[1]), str(e[2]), str(e[3]), str(e[4])))
    file.close()

def setPortfolio(user, port):
    file = open('data/%s-portfolio.txt' % user, 'w')
    for stock in port.keys():
        file.write('%s %s %s\n' %(stock, str(port[stock][0]), str(port[stock][1])))
    file.close()


# str -> void
def wallet(user):
    balance = getBalance(user)

    while True:
        command = input("You have an account balance of $%g \nWould you like to add, remove, or exit?\n" % balance).strip()
        if command == "add":
            #TODO: idiot proofing
            add = float(input("How much would you like to add to your account?\n").strip())
            balance += add
        elif command == "remove":
            add = float(input("How much would you like to remove from your account?\n").strip())
            if add <= balance:
                balance -= add
            else:
                print("You do not have that much money in your account.")
        elif command == "exit":
            setBalance(user, balance)
            break
