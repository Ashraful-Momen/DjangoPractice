from django.shortcuts import render
from django.http import HttpResponse 
from django.core.mail import EmailMessage,send_mail, mail_admins, send_mass_mail,BadHeaderError #for log main address use send_mass_mail
from templated_mail.mail import BaseEmailMessage
# Create your views here.

def calculate():
    x = 1
    y = 2
    return x

def say_hello(request):
    x = calculate()
    try:
        # send_mail('subject', 'message', 'info@shuvo.com',['bob@shuvo.com']) #From:	info@shuvo.com ; To:	bob@shuvo.com
        # mail_admins('subject','message plain text',html_message='hello sms')  

        #send Mail with file: -------------------------
        # message = EmailMessage('subject','message','from@shuvo.com', ['get@shuvo.com'])
        # message.attach_file('playground/static/img/MyIMG.jpg')
        # message.send()

        #Email with html page+dynamic Mail:---------------------------
        message = BaseEmailMessage(
            template_name='hello.html',
            context={'name':'Shuvo'}
        )
        message.send(['get@shuvo.com'])

    except BadHeaderError:
        pass
    return render(request, 'hello.html',{"name":"Shuvo"})
    # return HttpResponse("Hello World")




def sendMain(request):
    try:
        send_mail('subject', 'message', 'info@shuvo.com',['bob@shuvo.com'])
    except BadHeaderError:
        pass
    return render(request, 'hello.html',{"name":"Shuvo"})