from django.urls import path
from playground import views
app_name = 'playground'
urlpatterns = [
    path('hello/',views.say_hello, name='hello'),
    path('sendMain/',views.sendMain,name='sendMain')
]
