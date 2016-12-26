from celery import Celery
from tasks import *
from redis import Redis

r = Redis('localhost')

result = reverse.delay('antoni');
print result