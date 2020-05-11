from django.urls import path
from api import rapi

urlpatterns = [
    path('login', rapi.Login),
]