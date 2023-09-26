from django.dispatch import receiver
from store.singnals import order_created #__init.py form store.signal folder.


@receiver(order_created)
def on_order_created(sender,**kwargs):
    print(kwargs['order'])