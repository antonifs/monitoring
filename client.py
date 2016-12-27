from tasks import *
from redis import Redis

r = Redis('localhost')

result = serve.delay('antoni');
print result