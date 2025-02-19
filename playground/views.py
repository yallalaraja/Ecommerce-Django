from django.shortcuts import render
from django.core.mail import send_mail,mail_admins,BadHeaderError,EmailMessage
from templated_mail.mail import BaseEmailMessage
from .tasks import notify_customers

def say_hello(request):
    notify_customers('hii')
    return render(request,'hello.html',{'name':'raja'})

# def say_hello(request):
#     try:
        # send_mail('subject','message','info@rajabuy.com',['alice@rajabuy.com'])
        # mail_admins('subject','Message from admin',html_message='message')
        # message = EmailMessage('subject','message','from@rajasell.com',['harsha@rajasell.com'])
        # message.attach_file('playground/static/images/dog.jpg')
        # message.send()

    #     message = BaseEmailMessage(
    #         template_name='emails/hello.html',
    #         context = {'name':'ram'}
    #     )
    #     message.send(['harsha@good.com'])

    # except BadHeaderError:
    #     pass
    # return render(request,'hello.html',{'name':'Raja'})