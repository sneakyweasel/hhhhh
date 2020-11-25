import hashlib
from stickitup import SECRET_MIN
import pycurl
import psutil
import re
import os
from urllib.parse import urlencode
from functions import timeout_command_ex

# Generate sha1 hash with static prefix
def sha1gen(user):
  hash_object = hashlib.sha1(str.encode('SECRET_KEY' + user))
  pbHash = hash_object.hexdigest()
  return pbHash

# for i in range(0, 10):
#   user = "A"*i
#   print(f'USER: {user} -> SHA1: {sha1gen(user)}')

BINPATH = './bin/linux/'
data = "123456"
padding = "111"
user = "aaa"
signature = sha1gen(user)

cmd = [
  os.path.join(BINPATH, 'hash_extender'),
  '--data', f'{data}',
  '--secret-min', SECRET_MIN,
  '--append', f'{padding}',
  '--signature',  f'{signature}',
  '--format', 'sha1',
  '--out-data-format=hex',
  '--out-signature-format=hex',
  '--quiet'
]
print(cmd)
_, ret, data = timeout_command_ex(cmd, 10)
print("ret: {}, data: {}".format(ret, data))