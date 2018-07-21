from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST
from .models import SystemAdmin
from django.http import HttpResponse
from .forms import *
from django.contrib.auth.hashers import check_password
from django.contrib.auth import views

"""
def index(request):
    return render(request, 'systemAdmin/extensions/login.html', context={})
"""


def signup(request):
    if request.method == 'POST':
        f = AdminSignUpForm(request.POST)
        if f.is_valid():
            f.save()
            # messages.success(request, 'Account created successfully')
            return redirect('systemAdmin:login')

    else:
        f = AdminSignUpForm()
    return render(request, 'systemAdmin/extensions/signup.html', {'form': f})


def login(request):
    t = 'systemAdmin/extensions/login.html'
    f = AdminLoginForm(request.POST or None)

    if request.method == 'POST':
        if f.is_valid:
            username = request.POST['username'].lower()
            u = SystemAdmin.objects.filter(system_admin_user_name= username)
            if not u.count():
                uname_error = "There is no User with the supplied Username. \
                Please Enter your correct Username and Try again."
                return render(request,t,{'form':f, 'username_error': uname_error})

            password = request.POST['password']
            u1 = SystemAdmin.objects.get(system_admin_user_name= username)
            p = u1.get_password(password)
            if not p:
                password_error = "Invalid password. \
                Please Enter your correct Password and Try again."
                return render(request,t,{'form':f, 'password_error': password_error})


            user = f.get_user_id()
            request.session['user_admin'] = user
            print(user)
            return HttpResponse("You are now Logged in. Do you want to <a href='logout'>logout?</a>" + "\
            " + str(request.session['user_admin']))
    else:
        try:
            if request.session['user_admin']:
                return HttpResponse("You are Already Logged in. Do you want to <a href='logout'>logout?</a>" + str(f.uid))
                # return redirect('systemAdmin:login')
        except KeyError:

            f = AdminLoginForm()
    return render(request, t, {'form': f})


# LOGOUT METHOD.
def logout(request):
    try:
        del request.session['user_admin']
        return redirect('systemAdmin:login')
    except KeyError:
       return HttpResponse("Error.")

