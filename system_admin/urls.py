from django.urls import path
from django.contrib.auth.views import login
from . import views

app_name = 'system_admin'
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.admin_login, name='admin_login'),
    path('admin_login_process', views.admin_login_process, name='admin_login_process'),
    # path('login', login, {'template_name': 'system_admin/extensions/login.html'}),
]
