from django.urls import path
from . import views 

urlpatterns = [
    path('hello/',views.HelloView.as_view()),
    # path('hello2/',views.say_hello),
]