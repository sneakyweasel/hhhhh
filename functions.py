import logging
import psutil
import pycurl
import re

URL_REGISTER = 'http://stickitup.chall.malicecyber.com/register.php'
URL_LOGIN = 'http://stickitup.chall.malicecyber.com/login.php'
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
        c.setopt(pycurl.URL, URL_REGISTER + f"?alias={username}&email={email}&password={password}")
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
        return c.getinfo(pycurl.HTTP_CODE)
    finally:
        c.close()

def stick_login(email, password):
    try:
        c = pycurl.Curl() 
        c.setopt(pycurl.URL, URL_LOGIN + f"?email={email}&password={password}")
        c.setopt(pycurl.FOLLOWLOCATION, 1 )
        c.setopt(pycurl.HEADERFUNCTION, _write_header2)
        c.setopt(pycurl.WRITEFUNCTION, lambda x: None)
        c.setopt(pycurl.HTTPHEADER, [
            'Accept-Language: fr-fr', 
            'Upgrade-Insecure-Requests: 1', 
            'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15', 
            'Content-Type: application/x-www-form-urlencoded',
            'X-Requested-With: XMLHttpRequest',
            #'Set-Cookie: ' + SESSION
        ])
        c.perform()
        return c.getinfo(pycurl.HTTP_CODE)
    finally:
        c.close()