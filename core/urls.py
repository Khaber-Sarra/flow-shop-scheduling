from django.urls import  path
from .views import  index,create_instance,main,generate_instance, select_instance,logout
from.main_views import neh_view,chen_view,breach_and_bounds_view,tabu_search_view,ag_view,palmer_view
urlpatterns = [
    path('', index),
    path('main/', main),
    path('main/logout', logout),
    path('main/palmer', palmer_view),
    path('main/neh',neh_view),
    path("main/tabu_search",tabu_search_view),
    path('main/bb',breach_and_bounds_view),
    path('main/chen',chen_view),
    path('main/ag',ag_view),
    path('create', create_instance),
    path('generate', generate_instance),
    path('upload', select_instance)
]
