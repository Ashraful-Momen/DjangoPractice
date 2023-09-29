

#------------------------this code is work-------------------------------

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'storefront.settings')

app = Celery('storefront')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()




# -------------------------------------------------------------
# import os
# from celery import Celery

# #setup environment varible: as storefront.settings: 
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'storefront.settings')



# #create celery: 
# celery = Celery('storefront')

# #where celery find the setting : 
# celery.config_from_object('django.conf:settings',namespace='Celery')

# celery.autodiscover_tasks()


