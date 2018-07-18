from django.urls import path
from django.contrib.auth.views import login
from . import views

app_name = 'systemAdmin'
urlpatterns = [
    path('', views.adminLogin, name='adminLogin'),
    path('login', views.adminLogin, name='adminLogin'),
    path('loginProcess', views.loginProcess, name='loginProcess'),

    path('logout', views.logout, name='logout'),
    # path('login', login, {'template_name': 'system_admin/extensions/login.html'}),
]
