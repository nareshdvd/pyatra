#encoding:utf-8
import pika
import json

connection = pika.BlockingConnection(pika.URLParameters('amqp://pYaTrAuSeR:uSerpYAtra089@localhost:5672/pyatrarabbitmqvhost'))
channel = connection.channel()
channel.queue_declare(queue='my-queue', durable=True)

def send_realtime_info(key_val_dict):
  print "SENDING REALTIME INFO"
  json_value = json.dumps(key_val_dict)
  try:
    channel.basic_publish(exchange = '', routing_key ='my-queue' ,body = json_value ,properties=pika.BasicProperties(delivery_mode = 2,))
  except:
    print "Re-Opening the connection"
    connection = pika.BlockingConnection(pika.URLParameters('amqp://pYaTrAuSeR:uSerpYAtra089@localhost:5672/pyatrarabbitmqvhost'))
    channel = connection.channel()
    channel.queue_declare(queue='my-queue', durable=True)
    channel.basic_publish(exchange = '', routing_key ='my-queue' ,body = json_value ,properties=pika.BasicProperties(delivery_mode = 2,))