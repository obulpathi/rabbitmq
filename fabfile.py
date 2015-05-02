#!/usr/bin/env python

import pika
import string
import random
import timeit
import logging
from multiprocessing import Process

from fabric.api import env, hosts, get, put, sudo, run, cd, local, parallel


def random_string(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def create_vhosts(count = 1000):
    for i in range(count):
        vhost = random_string()
        local("rabbitmqctl add_vhost %s" % vhost)

def send(username = 'username', password = 'password',
         host='ip', port=5672, vhost='/', count = 10000):
    logging.basicConfig(level=logging.ERROR)

    credentials = pika.PlainCredentials(username, password)
    parameters = pika.ConnectionParameters(credentials=credentials,
                 host=host, port=port, virtual_host=vhost)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue='hello')
    for i in range(count):
        channel.basic_publish(exchange='',
                              routing_key='hello',
                              body='Hello World!')

    #print " [x] Sent 'Hello World!'"
    connection.close()


def receive(username = 'username', password = 'password',
    host='ip', port=5672, vhost='/'):
    logging.basicConfig(level=logging.ERROR)

    credentials = pika.PlainCredentials(username, password)
    parameters = pika.ConnectionParameters(credentials=credentials,
                 host=host, port=port, virtual_host=vhost)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    print ' [*] Waiting for messages. To exit press CTRL+C'

    def callback(ch, method, properties, body):
        print " [x] Received %r" % (body,)
        #if count == 10000:

    channel.basic_consume(callback,
                          queue='hello',
                          no_ack=True)

    channel.start_consuming()

def count(username = 'username', password = 'password',
    host='localhost', port=5672, vhost='vhost'):
    logging.basicConfig(level=logging.ERROR)

    credentials = pika.PlainCredentials(username, password)
    parameters = pika.ConnectionParameters(credentials=credentials,
                 host=host, port=port, virtual_host=vhost)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    print channel.queue_declare(queue='myqueue', passive= True)


def test(number = 1):
    print timeit.timeit(send, number = int(number))

def test1(number = 1):
    print timeit.timeit(send, number = int(number))

def test2(users = 10):
    processes = []
    for i in range(int(users)):
        process = Process(target = test)
        processes.append(process)
    for process in processes:
        process.start()
    for process in processes:
        process.join()

@parallel
#@hosts('root@rabbitmq-producer1')
@hosts('root@rabbitmq-producer1', 'root@rabbitmq-producer2', 'root@rabbitmq-producer3', 'root@rabbitmq-producer4', 'root@rabbitmq-producer5')
def update_local():
    put('/root/rabbitmq/fabfile.py', '/root/rabbitmq/fabfile.py')

@parallel
#@hosts('root@rabbitmq-producer1')
@hosts('root@rabbitmq-producer1', 'root@rabbitmq-producer2', 'root@rabbitmq-producer3', 'root@rabbitmq-producer4', 'root@rabbitmq-producer5')
def update():
    with cd('/root/rabbitmq'):
        run('git stash')
        run('git pull')
        run('git stash pop')

@parallel
#@hosts('root@rabbitmq-producer1')
@hosts('root@rabbitmq-producer1', 'root@rabbitmq-producer2', 'root@rabbitmq-producer3', 'root@rabbitmq-producer4', 'root@rabbitmq-producer5')
def copy():
    #put("/root/.gitconfig", "/root/.gitconfig")
    put('/root/rabbitmq/fabfile.py', '/root/rabbitmq/fabfile.py')
    put('/root/rabbitmq/makefile', '/root/makefile')

@parallel
@hosts('root@rabbitmq-producer1')
#@hosts('root@rabbitmq-producer1', 'root@rabbitmq-producer2', 'root@rabbitmq-producer3', 'root@rabbitmq-producer4', 'root@rabbitmq-producer5')
def test3(users = "1"):
    with cd('/root/rabbitmq'):
        run('fab test2:users=%s' % users)

@parallel
@hosts('root@rabbitmq-1vcpu-512mb')
#@hosts('root@rabbitmq-1vcpu-512mb', 'root@rabbitmq-1vcpu-1gb', 'root@rabbitmq-2vcpu-2gb', 'root@rabbitmq-2vcpu-4gb', 'root@rabbitmq-4vcpu-8gb', 'root@rabbitmq-6vcpu-15gb', 'root@rabbitmq-8vcpu-30gb')
def install():
    run('apt-get update')
    run('apt-get upgrade')
    run('apt-get install rabbitmq-server')
    run('rabbitmqctl add_user username password')
    run('rabbitmqctl add_vhost vhost')
    run('rabbitmqctl set_permissions -p /vhost username ".*" ".*" ".*")
