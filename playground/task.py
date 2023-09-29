from time import sleep
from celery import shared_task

@shared_task
def notify_customers(message):
    print('Task started')
    print('Sending 10k SMS')
    print(message)
    sleep(2)
    print('SMS were successfully sent')
    print('Task completed')
