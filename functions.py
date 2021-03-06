import logging
import psutil
import pycurl
import re
from io import BytesIO

URL_REGISTER = 'http://stickitup.chall.malicecyber.com/register.php'
URL_LOGIN = 'http://stickitup.chall.malicecyber.com/login.php'
URL_MEMBER = 'http://stickitup.chall.malicecyber.com/member.php'
URL_NOTES = 'http://stickitup.chall.malicecyber.com/notes.php'

BINPATH = './bin/macos/'
MAXLEN = 56

def timeout_command_ex(command, timeout, tmp=None, env={}, shell=False, universal_newlines=False, cast=True):
    """ Call shell-command and either return its output or kill it
    if it doesn't normally exit within <timeout> seconds

    :param command: command to be executed
    :type command: array
    :param timeout: watchdog timeout in seconds
    :type timeout: int
    :param tmp: temporary path
    :type tmp: str
    :return: None if process is aborted, subprocess, returncode and stdout otherwise
    """
    import subprocess, datetime, os
    cc = None

    if cast is True:
        command = [str(i) for i in command]
        print(' '.join(command))
    try:
        if tmp is None:
            cc = subprocess.run(command, timeout=timeout, check=True, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid, env=dict(os.environ, **env), universal_newlines=universal_newlines, close_fds=True)
        else:
            cc = subprocess.run(command, timeout=timeout, check=True, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid, cwd=str(tmp), env=dict(os.environ, **env), universal_newlines=universal_newlines, close_fds=True)
    except subprocess.TimeoutExpired:
        psutil.kill()
        logging.error("Command '%s' has timeout after %s seconds", command, timeout)
        return None, None, None

    return cc, cc.returncode, cc.stdout

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

def stick_register(username, email, password):
    try:
        c = pycurl.Curl() 
        url = URL_REGISTER
        print(url)
        c.setopt(pycurl.URL, url)
        c.setopt(pycurl.FOLLOWLOCATION, 1)
        c.setopt(pycurl.HEADERFUNCTION, _write_header1)
        c.setopt(pycurl.POST, 1)
        c#.setopt(pycurl.WRITEFUNCTION, lambda x: None)
        c.setopt(pycurl.POSTFIELDS, f"alias={username}&email={email}&password={password}")
        b = BytesIO()
        c.setopt(pycurl.WRITEDATA, b)
        c.setopt(pycurl.HTTPHEADER, [
            'Upgrade-Insecure-Requests: 1', 
            'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36', 
            'Content-Type: application/x-www-form-urlencoded',
            'Cookie: PHPSESSID=1lpibtq7ul54dalt90kak2lim7',
            'Cache-Control: max-age=0',
            'Origin: http://stickitup.chall.malicecyber.com',
            'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Referer: http://stickitup.chall.malicecyber.com/',
            'Accept-Language: fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7'
        ])
        c.perform() 
        return c.getinfo(pycurl.HTTP_CODE), b
    finally:
        c.close()

def stick_login(email, password):
    try:
        c = pycurl.Curl() 
        url = URL_LOGIN + f"?email={email}&password={password}"
        print(url)
        c.setopt(pycurl.URL, URL_LOGIN)
        c.setopt(pycurl.POST, 1)
        c.setopt(pycurl.FOLLOWLOCATION, 1 )
        c.setopt(pycurl.HEADERFUNCTION, _write_header2)
        #c.setopt(pycurl.WRITEFUNCTION, lambda x: None)
        c.setopt(pycurl.POSTFIELDS, f"email={email}&password={password}")
        b = BytesIO()
        c.setopt(pycurl.WRITEDATA, b)
        c.setopt(pycurl.HTTPHEADER, [
            'Accept-Language: fr-fr', 
            'Upgrade-Insecure-Requests: 1', 
            'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15', 
            'Content-Type: application/x-www-form-urlencoded',
            'X-Requested-With: XMLHttpRequest',
            #'Set-Cookie: ' + SESSION
        ])
        c.perform()
        return c.getinfo(pycurl.HTTP_CODE), b
    finally:
        c.close()

def stick_member(prepend, signature, prefix='admi'):

    auth=prepend + '%3A' + signature
    print(auth)
    try:
        c = pycurl.Curl() 
        url = URL_MEMBER
        print(url)
        c.setopt(pycurl.URL, URL_LOGIN)
        c.setopt(pycurl.FOLLOWLOCATION, 1 )
        #c.setopt(pycurl.WRITEFUNCTION, lambda x: None)
        b = BytesIO()
        c.setopt(pycurl.WRITEDATA, b)
        c.setopt(pycurl.HTTPHEADER, [
            'Accept-Language: fr-fr', 
            'Upgrade-Insecure-Requests: 1', 
            'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15', 
            'Content-Type: application/x-www-form-urlencoded',
            'X-Requested-With: XMLHttpRequest',
            'Cookie: auth=' + auth
        ])
        print('Cookie: auth=' + auth)
        c.perform()
        return c.getinfo(pycurl.HTTP_CODE), b
    finally:
        c.close()

def stick_note(prepend, signature, prefix='admi'):

    auth=prepend + '%3A' + signature
    print(auth)
    try:
        c = pycurl.Curl() 
        url = URL_NOTES
        print(url)
        c.setopt(pycurl.URL, URL_LOGIN)
        c.setopt(pycurl.FOLLOWLOCATION, 1 )
        #c.setopt(pycurl.WRITEFUNCTION, lambda x: None)
        b = BytesIO()
        c.setopt(pycurl.WRITEDATA, b)
        c.setopt(pycurl.HTTPHEADER, [
            'Accept-Language: fr-fr', 
            'Upgrade-Insecure-Requests: 1', 
            'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15', 
            'Content-Type: application/x-www-form-urlencoded',
            'X-Requested-With: XMLHttpRequest',
            'Cookie: auth=' + auth
        ])
        print('Cookie: auth=' + auth)
        c.perform()
        return c.getinfo(pycurl.HTTP_CODE), b
    finally:
        c.close()