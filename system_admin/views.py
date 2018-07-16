from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from .models import *
from django.contrib.auth.views import login
from django.http import HttpResponse

from .forms import *


def index(request):
    return render(request, 'system_admin/extensions/login.html', context={})
#    return HttpResponse("Hello, world. You're welcome @ the orims index page.<br/>Page is still under construction")


def admin_login(request):
    login_form = AdminLoginForm()
    return render(request, 'system_admin/extensions/login.html', context={'form': login_form})


@require_POST  # To only allow Post requests from client side
def admin_login_process(request):

    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        # create a form instance and populate it with data from the request:
        form = AdminLoginForm(request.POST)

        # check whether form instance is created:
        if form:
            # process the data in form.cleaned_data as required
            user = get_object_or_404(SystemAdmin, system_admin_user_name=request.POST['username'])
            print(user)

            # Destroy the form by Creating empty instance
            form = AdminLoginForm()

            if not user:
                return render(request, 'system_admin/extensions/login.html', context={})

            # redirect to a new URL:
            return render(request, 'system_admin/extensions/index.html', context={})

        # Create empty form for Login
        else:
            form = AdminLoginForm()
            return render(request, 'system_admin/extensions/login.html', context={'form': form})
        # End if form:

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AdminLoginForm()
        return render(request, 'system_admin/extensions/login.html', context={'form': form})
    # End if request.method == 'POST':


"""
    if login_form.is_valid():
        user = SystemAdmin.system_admin_user_name(system_admin_user_name=login_form.cleaned_data['username'])
        if user:
            print('No user found')
            return render(request, 'system_admin/base/base.html', context={'form': login_form})
        # end if user:
        if user.system_admin_password == login_form.cleaned_data['password']:
            request.session['member_id'] = user.system_admin_id
            print('You are logged in')
            return render(request, 'system_admin/base/base.html', context={'form': login_form})
        else:
            # return HttpResponse("Your username and password didn't match.")
            print('No user')
            return render(request, 'system_admin/extensions/login.html', context={'form': login_form})
        # End if user.password == request.POST['password']:
    else:
        print('Invalid data')
        return render(request, 'system_admin/base/base.html', context={'form': login_form})
    # End if login_form.is_valid():
"""