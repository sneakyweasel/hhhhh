# hello
from os import stat
import hashpumpy
import urllib.parse

from functions import stick_register, stick_login

def main():
    # admi / '4dd28ad0560441245de6fda3973890eeb41b702d' / variable key length
    results = []
    for i in range(6, 30):
        data = hashpumpy.hashpump('4dd28ad0560441245de6fda3973890eeb41b702d', "admi", 'n', i)
        results.append(data)

    for r in results:
        register_user = urllib.parse.quote_from_bytes(r[1])
        print("{} => {}".format(r[0], register_user))

        register_user = "alamo"
        register_email = f'{register_user}%40pwn.com'
        register_pwd   = "tototo"
        status, data = stick_register(register_user, register_email, register_pwd)
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