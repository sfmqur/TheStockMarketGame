import os

# init code
# load user accounts
users = []
if os.path.exists('data/users.txt'):
    file = open('data/users.txt', 'r')
    for l in file:
        print(l)
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

print("User: %s" % user)

# run loop
while run:
    # load user data
    # asks for command
    command = input('What would you like to do? \nhelp for help')
    # if command exit, cleanup
    if command == 'help':
        print('here is your help')
    elif command == 'exit':
        run = False
        # cleanup code here
        # write user data
    else:
        print('That command does not exist.')


# exit code
# save accounts to file
file = open('data/users.txt', 'w')
for u in users:
    file.write('%s\n'% u)
file.close()
