from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST
from .models import SystemAdmin
from django.utils import timezone
from django.http import HttpResponse
from .forms import *
from orims.views import *
from django.contrib.auth.hashers import check_password
from django.contrib.auth import views

"""
def index(request):
    return render(request, 'systemAdmin/extensions/login.html', context={})
"""


def signup(request):
    if request.method == 'POST':
        f = AdminSignUpForm(request.POST)
        t = 'systemAdmin/extensions/signup.html'
        if f.is_valid():
            f.save()
            f = AdminSignUpForm()
            return render(request, t, {'form': f,'display_success':True})
        # End of if f.is_valid():
    else:
        f = AdminSignUpForm()
    # End of if request.method == 'POST':

    return render(request, 'systemAdmin/extensions/signup.html', {'form': f})
# End of function signup():


def login(request):
    t = 'systemAdmin/extensions/login.html'
    f = AdminLoginForm(request.POST or None)
    context = {'form':f}
    if request.method == 'POST':
        if f.is_valid:
            username = request.POST['username'].lower()
            u = SystemAdmin.objects.filter(system_admin_user_name= username)
            if not u.count():
                uname_error = "There is no User with the supplied Username. \
                Please Enter your correct Username and Try again."
                context.update({'username_error': uname_error})
                return render(request, t, context)
            # End of if not u.count():

            password = request.POST['password']
            u1 = SystemAdmin.objects.get(system_admin_user_name= username)
            p = u1.get_password(password)
            if not p:
                password_error = "Invalid password. \
                Please Enter your correct Password and Try again."
                context.password_error = password_error
                context.update({'password_error': password_error})
                return render(request, t, context)
            # End of if not p:

            user = u1.get_user_id()
            request.session['user_admin'] = user
            t = 'systemAdmin/extensions/home.html'
            return render(request, t, context)
        # End of if f.is_valid:
    else:
        try:
            if request.session['user_admin']:

                set_ssession_data(request, request.session['user_admin'])
                return redirect('systemAdmin:home')
        except KeyError:
            f = AdminLoginForm()
        context.update({'form': f})
        # End of try:
    return render(request, t, context)
# End of function login():


# SYSTEM ADMIN HOME PAGE BUILDER
def home(request):
    # STEP1.0.0: Set home template.
    t = 'systemAdmin/extensions/home.html'
    context = {'units': ''}

    # STEP1.1: Test for session, to determine currently logged in user.
    # if user is logged in, build home page.
    try:
        if request.session['user_admin']:
            user = request.session['user_admin']
            set_ssession_data(request, user)
            units = fetch_units_for_user(user)
            context.update({'units': units})
            return render(request, t, context)
        else:
            # if no user is logged in, redirect to Login page.
            return redirect('systemAdmin:login')
        # End of if request.session['user_admin']:
    except KeyError:
        pass
    # End of try:
    return redirect('systemAdmin:login')
# End of function home():


# LOGOUT METHOD.
def logout(request):
    try:
        if request.session['user_admin']:
            del request.session['user_admin']

        if request.session['user_staff']:
            del request.session['user_staff']

        if request.session['current_time']:
            del request.session['current_time']
        return redirect('systemAdmin:login')
    except KeyError:
       return HttpResponse("Error.")
# End of function logout():


# CHECK ADMIN LOGIN STATUS EVERY TIME BEFORE LOADING ANY TEMPLATE
def loggedin(request, template, data_feed):
    # STEP1.0: Receive and store passed template(template) in local variable t.
    t = template

    # STEP1.0: Receive and store passed data feed in local variable df.
    df = data_feed

    # STEP2.0: Test for running session, to determine if there is any logged in user(user_admin).
    # Using the try concept, to handle omissions in case no session instance is found.
    try:
        # if there is any user logged in, return appropriate template and data_feeds.
        if request.session['user_admin']:
            return render(request, t,)

        # if no user is logged in, redirect to Login page.
        else:
            return redirect('systemAdmin:login')
        # End if request.session['user_admin']:

    # Throw keyError as exception just in case.
    except KeyError:
        # If all is well, just do nothing.
        pass
    # Failure to successfully execute this code, just load the home page.
    return redirect('systemAdmin:login')
    # End of try
# End of function loggedin():


# Fetch user details based on session admin id
# This data is always to be fetched frequently before any action.
# This is because, in case the user data is updated, the session is updated too.
def set_ssession_data(request, uid):
    if uid:
        u = SystemAdmin.objects.get(system_admin_id=uid)
        admn = {
            'userid': uid,
            'username': u.system_admin_user_name,
            'role': 'Administrator',
            'email': u.system_admin_email,
            # 'photo': u.system_admin_user_name,
        }
        request.session['admin'] = admn
        t= timezone.now().date().year
        # 'year': timezone.now().date().year,
        # 'month': timezone.now().date().month,
        # 'day': timezone.now().date().day,
        # 'weekday': timezone.now().date().isoweekday(),
        # 'hour': timezone.now().time().hour,
        # 'minute': timezone.now().time().minute,
        # 'second': timezone.now().time().second,
        # 'microsecond': timezone.now().time().microsecond,
        # 'meridian': timezone.now().time(),
        request.session['current_time'] = t
# End of def set_ssession_data()
