from django.urls import path
from . import views

# app_name = 'orims'
urlpatterns = [
    path('', views.index, name='index'),
    # path('', views.index, name='index'),
]