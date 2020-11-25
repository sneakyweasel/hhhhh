import hashlib

# Generate sha1 hash with static prefix
def sha1gen(user):
  hash_object = hashlib.sha1(str.encode('SECRET_KEY' + user))
  pbHash = hash_object.hexdigest()
  return pbHash

for i in range(0, 10):
  user = "A"*i
  print(f'USER: {user} -> SHA1: {sha1gen(user)}')