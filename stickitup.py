import pycurl
import re
import os
from urllib.parse import urlencode

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
    try:
        if tmp is None:
            cc = subprocess.run(command, timeout=timeout, check=True, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid, env=dict(os.environ, **env), universal_newlines=universal_newlines, close_fds=True)
        else:
            cc = subprocess.run(command, timeout=timeout, check=True, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid, cwd=str(tmp), env=dict(os.environ, **env), universal_newlines=universal_newlines, close_fds=True)
    except subprocess.TimeoutExpired:
        process.kill()
        if job_id is None:
            logging.error("Command '%s' has timeout after %s seconds", command, timeout)
        else:
            logging.error("#%s Command '%s' has timeout after %s seconds", job_id, command, timeout)
        return None, None, None

    return cc, cc.returncode, cc.stdout
