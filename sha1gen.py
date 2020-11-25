import hashlib
import pycurl
import psutil
import re
import os
import sys
from urllib.parse import urlencode

#sys.path.append('./site-packages/')

from functions import timeout_command_ex

# Generate sha1 hash with static prefix
def sha1gen(user):
  hash_object = hashlib.sha1(str.encode('SECRET_KEY' + user))
  pbHash = hash_object.hexdigest()
  return pbHash

def main():
  BINPATH = './bin/macos/'
  data = "123456"
  padding = "111"
  user = "aaa"
  signature = sha1gen(user)

  cmd = [
    os.path.join(BINPATH, 'hash_extender'),
    '--data', f'{data}',
    '--secret-min', "6",
    '--secret-max', '10',
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