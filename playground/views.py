from django.shortcuts import render

from .task import notify_customers  # Make sure you import the correct task

def say_hello(request):

    # Queue the Celery task for sending message. Use .delay() instead of .dely()
    notify_customers.delay(message="Try another sms print")

    return render(request, 'hello.html', {"name": "Shuvo"})



