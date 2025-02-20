import requests
from django.shortcuts import render
from django.core.cache import cache
from django.core.mail import send_mail,mail_admins,BadHeaderError,EmailMessage
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from templated_mail.mail import BaseEmailMessage
from .tasks import notify_customers

class HelloView(APIView):
    @method_decorator(cache_page(5*60))
    def get(self,request):
        response = requests.get('https://httpbin.org/delay/2')
        data = response.json()
        return render(request,'hello.html',{'name':'raja'})

# @cache_page(5*60)
# def say_hello(request):
#     response = requests.get('https://httpbin.org/delay/2')
#     data = response.json()
#     return render(request,'hello.html',{'name':'raja'})


def say_hello(request):
    key = 'httpbin_result'
    if cache.get(key) is None:
        response = requests.get('https://httpbin.org/delay/2')
        data = response.json()
        cache.set(key,data)
    return render(request,'hello.html',{'name':cache.get(key)})


# def say_hello(request):
#     notify_customers('hii')
#     return render(request,'hello.html',{'name':'raja'})

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