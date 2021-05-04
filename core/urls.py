from django.urls import  path
from .views import  index,create_instance,main
urlpatterns = [
    path('', index),
    path('main/', main),
    path('create', create_instance)
]
