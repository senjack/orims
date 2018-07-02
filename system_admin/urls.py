from django.urls import path
from . import views

app_name = 'system_admin'
urlpatterns = [
    path('', views.index, name='index'),
]
