import os
import gameFunctions as gf

# init code
run = False
# load user accounts
users = []
if os.path.exists('data/users.txt'):
    file = open('data/users.txt', 'r')
    for l in file:
        users.append(l.strip())
    file.close()

# login code
while True:
    # ask user for account
    user = input('Input your user name, exit to exit.\n')
    user = user.strip()
    # if account exists login
    if user in users:
        run = True
        break
    # else ask to create account
    elif user == 'exit':
        break
    else:
        response = input('That account does not exist. Would you like to create it? [y/n]\n')
        response = response.strip()
        if response == 'y':
            users.append(user)
            run = True
            break

# save accounts to file
file = open('data/users.txt', 'w')
for u in users:
    file.write('%s\n' % u)
file.close()

print("User: %s" % user)

# run loop
while run:
    # asks for command
    command = input('What would you like to do? ')
    # transaction history command
    if command == 'history':
        gf.showHistory(user)

    elif command == 'quote':
        # TODO: idiot proofing, program crashes when a symbol that doesn't exist is inputted
        symbol = input('What symbol are you looking for? ').strip().upper()
        quote = gf.getQuote(symbol)
        print("%s is trading for %g per share" % (symbol, quote))

    # buy stock command, symbol and num shares
    elif command == 'buy':
        symbol = input('What symbol are you buying? ')
        numShares = input('How many shares would you like to buy? ')
        # TODO: idiot checking
        numShares = int(numShares.strip())
        gf.buyStock(user, symbol, numShares)

    # sell stock command, symbol and num shares
    elif command == 'sell':
        symbol = input('What symbol are you selling? ')
        numShares = input('How many shares would you like to sell? ')
        # TODO: idiot checking
        numShares = int(numShares.strip())
        gf.sellStock(user, symbol, numShares)

    # see portfolio
    elif command == 'portfolio':
        gf.showPortfolio(user)

    elif command == 'help':
        print('Commands: quote, buy, sell, portfolio, history, exit')

    elif command == 'exit':
        run = False
        # cleanup code here
        # write user data
    else:
        print('That command does not exist. Type help for help')


# exit code

