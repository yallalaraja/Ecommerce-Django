from time import sleep 
from celery import shared_task

@shared_task
def notify_customers(message):
    print('sending 10k mails')
    print(message)
    sleep(3)
    print('Email successfully sent')