from django.urls import  path
from .views import  index,create_instance,main,generate_instance, select_instance
from.main_views import neh
urlpatterns = [
    path('', index),
    path('main/', main),
    path('main/neh',neh),
    path('create', create_instance),
    path('generate', generate_instance),
    path('upload', select_instance)
]
