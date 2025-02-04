from django.shortcuts import render
from django.core.mail import send_mail,mail_admins,BadHeaderError

def say_hello(request):
    try:
        # send_mail('subject','message','info@rajabuy.com',['alice@rajabuy.com'])
        mail_admins('subject','Message from admin',html_message='message')
    except BadHeaderError:
        pass
    return render(request,'hello.html',{'name':'Raja'})