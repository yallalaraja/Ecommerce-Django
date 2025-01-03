from django.urls import path
from . import views 

urlpatterns = [
    path('say_hello/',views.hello)
]