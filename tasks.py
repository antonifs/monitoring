from celery import Celery

# app = Celery('tasks', broker='amqp://localhost//', backend='db+mysql://rabbitmq1:rabbitmq1@localhost/rabbitmq1')
app = Celery('tasks', backend='redis://127.0.0.1', broker='amqp://guest@127.0.0.1//')

@app.task
def reverse(string):
    return string[::-1]