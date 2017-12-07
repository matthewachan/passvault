# Import dependencies
import sys
import getpass
from cryptography.fernet import Fernet
from termcolor import colored, cprint
from pyfiglet import figlet_format

# Custom colored print function
def c_print(text):
    return cprint(text, t_color)

# Custom colored raw_input
def c_raw_input(text):
    return raw_input(colored(text, t_color))

# Custom colored hidden input
def c_getpass(text):
    return getpass.getpass(colored(text, t_color))


# Set stdout text color
t_color = 'white'
# Path to .passvault.txt
path = '/Users/mchan/Documents/GitHub/passvault/.passvault.txt'
# Placeholder value for username
uname = 'placeholder'



# Print ASCII art
c_print(figlet_format('passvault', font='chunky'))
# Prompt user for key 
key = c_getpass('Enter key: ').strip()
# Object for encrypting and decrypting text
cipher_tool = Fernet(key)

# Read usernames/passwords from textfile
passvault = dict() 
with open(path, 'r') as pv:
    for line in pv:
        (user, pw) = line.split()
        # Decrypt user/password pairs
        user = cipher_tool.decrypt(user)
        pw = cipher_tool.decrypt(pw)
        passvault[user] = pw

while uname != 'e':
    uname = c_raw_input('Username to lookup or (e)xit: ')
    if uname == 'e':
        c_print('Exiting...')
        break
    # Print password if found
    if uname in passvault.keys():
        c_print('Matching password is ' + passvault[uname])
    else:
        c_print('No matching password found.')
        action = c_raw_input('Would you like to add this as a new user? (y)es/(n)o ')
        if action == 'y':
            new_pass = c_getpass('Enter password: ')
            passvault[uname] = new_pass
            c_print('Username/password saved!')

# Overwrite passvault file
with open(path, 'w') as pv:
    for key, value in passvault.items():
        pv.write(cipher_tool.encrypt(key.strip()) + ' ' + cipher_tool.encrypt(value.strip()) + '\n')
