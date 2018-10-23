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

    path('home', views.home, name='home'),

    path('serviceUnits', views.serviceUnits, name='serviceUnits'),

    path('serviceUnits?user=system-admin&level=system_admin&action=create_unit&mode=load_form', views.serviceUnits, name='serviceUnits'),

    path('serviceUnits?user=system-admin&level=system_admin&action=cancel_unit_creation&mode=hide_form', views.serviceUnits, name='serviceUnits'),

    path('serviceUnits?user=system-admin&level=system_admin&action=view_units', views.serviceUnits,name='serviceUnits'),

    path('createUnit', views.createUnit, name='createUnit'),

    path('editUnit', views.editUnit, name='editUnit'),

    path('editUnit/<int:unit_id>/', views.editUnit, name='editUnit'),

    path('updateUnit', views.updateUnit, name='updateUnit'),

    path('updateUnit/<int:unit_id>/', views.updateUnit, name='updateUnit'),

    path('deleteUnit', views.deleteUnit, name='deleteUnit'),

    path('deleteUnit/<int:unit_id>/', views.deleteUnit, name='deleteUnit'),

    path('userAccounts', views.userAccounts, name='userAccounts'),

    path('editAdmin', views.editAdmin, name='editAdmin'),

    path('updateAdmin', views.updateAdmin, name='updateAdmin'),

    path('updateAdmin/<int:admin_id>/', views.updateAdmin, name='updateAdmin'),

    path('appointments', views.appointments, name='appointments'),

    path('logout', views.logout, name='logout'),
    # path('login', login, {'template_name': 'system_admin/extensions/login.html'}),
]
