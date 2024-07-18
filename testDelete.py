import redis
 
r = redis.Redis(host='localhost', port=6379, db=10)
 
pattern = 'qunguan_user_in_group_first_time*'
 
for key in r.scan_iter(match=pattern):
    r.delete(key)
    print(key)