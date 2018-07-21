from django.urls import path
from django.contrib.auth.views import login
from . import views

app_name = 'systemAdmin'
urlpatterns = [
    path('', views.login, name='login'),

    path('signup', views.signup, name='signup'),
    # path('registration', views.registration, name='registration'),

    path('login', views.login, name='login'),
    # path('login_process', views.login_process, name='login_process'),

    path('logout', views.logout, name='logout'),
    # path('login', login, {'template_name': 'system_admin/extensions/login.html'}),
]
