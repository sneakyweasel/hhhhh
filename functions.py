import logging
import psutil

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