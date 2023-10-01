from django.urls import path
from playground import views

app_name = 'playground'

urlpatterns = [
    path('hello/', views.SayHello.as_view(), name='hello'),
]
