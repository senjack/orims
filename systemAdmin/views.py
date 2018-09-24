from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from .forms import *
from orims.views import *
from orims.forms import *
from .models import SystemAdmin
from orims.meta import meta_data
from django.http.response import HttpResponse
from django.http.request import HttpRequest
from django.core.files import uploadedfile
from django.views.decorators.http import require_POST
from django.contrib.auth.hashers import check_password
from django.contrib.auth import views

"""
def index(request):
    return render(request, 'systemAdmin/extensions/login.html', context={})
"""


def signup(request):
    # Test whether POST method is used.
    # POST method is needed for data hiding
    if request.method == 'POST':
        # If the POST method was used, then create and set Variables(filled up form and template).
        # Create a new form instance(f)
        f = AdminSignUpForm(request.POST)
        t = 'systemAdmin/extensions/signup.html'
        # Check for form validity(status)
        if f.is_valid():
            # If form is valid, then save data in the form and and then clear the signUp form,
            #  by creating a new empty signUp form instance.
            f.save()
            f = AdminSignUpForm()
            # Now return the empty Signup form with success message alert initiated.
            return render(request, t, {'form': f,'display_success':True})
        # End of if f.is_valid():
    else:
        # If the POST method was not used, then Drop or clear up that insecure data,
        # By creating an empty signUp form instance.
        # OR in case of first signup instance, Prepare an empty signup form.
        f = AdminSignUpForm()
    # End of if request.method == 'POST':

    # In case of first signup instance, Return an empty SignUp form.
    return render(request, 'systemAdmin/extensions/signup.html', {'form': f})
# End of function signup():


def login(request):
    # Sert login template.
    t = 'systemAdmin/extensions/login.html'
    # If the Request POST variable has data in it, Create a filled up Login form instance(f).
    # Otherwise set f to nothing.
    f = AdminLoginForm(request.POST or None)
    # set f as a value to the key 'form' of the context object to be passed on to any returned template
    context = {'form':f}
    if request.method == 'POST':
        # In case the request.POST variable has some data, Test for validity of the passed data.
        if f.is_valid:
            # If data in the Request.POST variable is valid, fetch user name from the form.
            username = request.POST['username'].lower()
            # Check whether there is any user with the supplied user name.
            u = SystemAdmin.objects.filter(system_admin_user_name= username)
            if not u.count():
                # In case there is no user with the supplied user name set username error
                uname_error = "There is no User with the supplied Username. \
                Please Enter your correct Username and Try again."
                context.update({'username_error': uname_error})
                # Terminate the login process and throw username error.
                return render(request, t, context)
            # End of if not u.count():

            # In case there is a user with the supplied username,
            # fetch the supplied password form the submitted form.
            password = request.POST['password']
            u1 = SystemAdmin.objects.get(system_admin_user_name= username)
            # Compare the supplied password with that of the filtered user from the database.
            p = u1.get_password(password)
            if not p:
                # In case the two password don't tally or match, set password error
                password_error = "Invalid password. \
                Please Enter your correct Password and Try again."
                context.update({'password_error': password_error})
                # Terminate the login process and throw password error
                return render(request, t, context)
            # End of if not p:

            # In case the two passwords match, then the authentication process was successful.
            # Hence set or start the user session for admin.
            user = u1.get_user_id()
            request.session['user_admin'] = user
            # After the system admin user session has been successfully set, then redirect to System-admin home.
            return redirect('systemAdmin:home')
        # End of if f.is_valid:
    else:
        # In case no data was submitted,.
        try:
            # Test for any logged in user.
            if request.session['user_admin']:
                # In case of a logged in user, redirect to System admin home.
                return redirect('systemAdmin:home')
        except KeyError:
            # Else create an empty login form for logging in.
            f = AdminLoginForm()
        context.update({'form': f})
        # End of try:
    # Return the new created empty login form.
    return render(request, t, context)
# End of function login():


# SYSTEM ADMIN HOME PAGE BUILDER
def home(request):
    # STEP1.0.0: Set home template and create an empty context object.
    t = 'systemAdmin/extensions/home.html'
    context = {}
    # STEP1.1: Test for session, to determine currently logged in user.
    try:
        if request.session['user_admin']:
            # if user is logged in, build home page.
            # create new user instance
            user = request.session['user_admin']
            # Set session data for the new user
            set_session_data(request, user)
            # Fetch and set all service units created or managed by the current user.
            units = fetch_units_for_user(user)
            context.update({'units': units})
            # Build and return the home client view template with the set units for the user
            return render(request, t, context)
        else:
            # if no user is logged in, try Logging in.
            return redirect('systemAdmin:login')
        # End of if request.session['user_admin']:
    except KeyError:
        # In case  testing for the logged in user fails, try nothing,
        pass
    # End of try:
    # Just try logging in.
    return redirect('systemAdmin:login')
# End of function home():


# OFFIECE ACCOUNTS MANAGEMENT OPTIONS PAGE BUILDER
def serviceUnits(request):
    # STEP1.0.0: Set template and create an empty context object.
    t = 'systemAdmin/extensions/service_units.html'
    context = {}
    f = UnitCreationForm(request.POST or None)

    # STEP1.1: Test for session, to determine currently logged in user.
    try:
        if request.session['user_admin']:
            # if user is logged in, build the required page.
            # create new user instance
            user = request.session['user_admin']
            # Set session data for the new user
            set_session_data(request, user)
            if request.GET and request.GET['user'] == 'system-admin' and request.GET['level'] == 'system_admin':
                if request.GET['action'] == 'create_unit' and request.GET['mode'] == 'load_form':
                    # Fetch and set all service units created or managed by the current user.
                    t = 'systemAdmin/extensions/mono_page.html'
                    units = fetch_units_for_user(user)
                    context.update({'units': units})
                    context.update({'create_unit': True})
                    if request.method == 'POST':
                        if f.is_valid():
                            pass
                    else:
                        context.update({'form': f})

                elif request.GET['action'] == 'cancel_unit_creation' and request.GET['mode'] == 'hide_form':
                    # Empty all form fields:
                    f = UnitCreationForm()
                    return redirect('systemAdmin:serviceUnits')
                elif request.GET['action'] == 'view_units':
                    # Fetch and set all service units created or managed by the current user.
                    units = fetch_units_for_user(user)
                    context.update({'units': units})
                    context.update({'section_title_info': 'A list of All Service units you manage.'})
                    context.update({'toggle_title1': 'Select this Service unit for more Management options'})
                    context.update({'btn1_value': 'glyphicon glyphicon-thumbs-up'})
                    context.update({'toggle_title2': 'Edit this Service unit\'s Information'})
                    context.update({'btn2_value': 'glyphicon glyphicon-pencil clr-gre'})
                    context.update({'toggle_title3': 'Delete this Service unit?'})
                    context.update({'btn3_value': 'glyphicon glyphicon-trash clr-gre1'})
                    context.update({'display_unit_selection_list': True})
                    context.update({'branches': ''})
                else:
                    # Fetch and set all service units created or managed by the current user.
                    units = fetch_units_for_user(user)
                    branches = []
                    for unit in units:
                        branches.append(fetch_branches_for_units(unit.unit_id))
                    branches = branches

                    context.update({'units': units})
                    context.update({'branches': branches})
                    context.update({'section_title_info': 'You can view appointments for the entire Service unit, or browse for Branches under it.'})
                    context.update({'toggle_title1': 'View Appointments for this entire Service unit'})
                    context.update({'btn1_value': 'glyphicon glyphicon-eye-open'})
                    context.update({'toggle_title2': 'Browse Branches under this Service unit'})
                    context.update({'btn2_value': 'glyphicon glyphicon-option-horizontal clr-grn'})
                # End if
                # Build and return the required page
                return render(request, t, context)
            else:
                # In case of no GET request, just load service unit options
                return render(request, t, context)
        else:
            # if no user is logged in, try Logging in.
            return redirect('systemAdmin:login')
        # End of if request.session['user_admin']:
    except KeyError:
        # In case  testing for the logged in user fails, try nothing,
        pass
    # End of try:
    # Just try logging in.
    return redirect('systemAdmin:login')
# End of officeAccounts() Method


# USER ACCOUNTS MANAGEMENT OPTIONS PAGE BUILDER
def createUnit(request):
    # STEP1.0.0: Set template and create an empty context object.
    t = 'systemAdmin/extensions/service_units.html'
    context = {}
    f = UnitCreationForm(request.POST, request.FILES)

    # STEP1.1: Test for session, to determine currently logged in user.
    try:
        if request.session['user_admin']:
            # if user is logged in, build the required page.
            # create new user instance
            user = request.session['user_admin']
            # Set session data for the new user
            set_session_data(request, user)
            if request.POST and f is not None:
                # f.set_admin_id(user)
                if f.is_valid():
                    instance = f.save(commit=False)
                    us = SystemAdmin.objects.get(system_admin_id = user)
                    instance.system_admin_id = us
                    instance.save()
                    print("Service unit registered succesfully : " + str(instance))
                    return HttpResponse("Service unit registered succesfully " + str(instance))
            else:
                return HttpResponse("<font color = 'red'><b>Invalid data Submitted</b></font>")
            # Build and return the required page
            return render(request, t, context)
        else:
            # if no user is logged in, try Logging in.
            return redirect('systemAdmin:login')
        # End of if request.session['user_admin']:
    except KeyError:
        # In case  testing for the logged in user fails, try nothing,
        pass
    # End of try:
    # Just try logging in.
    return redirect('systemAdmin:login')


# USER ACCOUNTS MANAGEMENT OPTIONS PAGE BUILDER
def userAccounts(request):
    # STEP1.0.0: Set template and create an empty context object.
    t = 'systemAdmin/extensions/user_accounts.html'
    context = {}

    # STEP1.1: Test for session, to determine currently logged in user.
    try:
        if request.session['user_admin']:
            # if user is logged in, build the required page.
            # create new user instance
            user = request.session['user_admin']
            # Set session data for the new user
            set_session_data(request, user)
            # Build and return the required page
            return render(request, t, context)
        else:
            # if no user is logged in, try Logging in.
            return redirect('systemAdmin:login')
        # End of if request.session['user_admin']:
    except KeyError:
        # In case  testing for the logged in user fails, try nothing,
        pass
    # End of try:
    # Just try logging in.
    return redirect('systemAdmin:login')
# End of userAccounts() Method


# APPOINTMENT RECORDS MANAGEMENT OPTIONS PAGE BUILDER
def appointments(request):
    # STEP1.0.0: Set template and create an empty context object.
    t = 'systemAdmin/extensions/appointments.html'
    context = {}

    # STEP1.1: Test for session, to determine currently logged in user.
    try:
        if request.session['user_admin']:
            # if user is logged in, build the required page.
            # create new user instance.
            user = request.session['user_admin']
            # Set session data for the new user
            set_session_data(request, user)
            # Fetch and set all service units created or managed by the current user.
            units = fetch_units_for_user(user)
            branches = []
            for unit in units:
                branches.append(fetch_branches_for_units(unit.unit_id))
            branches = branches

            context.update({'units': units})
            context.update({'branches': branches})
            context.update({'section_title_info': 'You can view appointments for the entire Service unit, or browse for Branches under it.'})
            context.update({'toggle_title1': 'View Appointments for this entire Service unit'})
            context.update({'btn1_value': 'glyphicon glyphicon-eye-open'})
            context.update({'toggle_title2': 'Browse Branches under this Service unit'})
            context.update({'btn2_value': 'glyphicon glyphicon-option-horizontal clr-grn'})
            # Build and return the required page
            return render(request, t, context)
        else:
            # if no user is logged in, try Logging in.
            return redirect('systemAdmin:login')
        # End of if request.session['user_admin']:
    except KeyError:
        # In case  testing for the logged in user fails, try nothing,
        pass
    # End of try:
    # Just try logging in.
    return redirect('systemAdmin:login')
# End of appointments() Method


# LOGOUT METHOD.
def logout(request):
    """ THE LOGOUT PROCESS """
    try:
        if request.session['user_admin']:
            # Logout any system-admin currently logged in
            del request.session['user_admin']
        # END: if request.session['user_admin']:

        if request.session['user_receptionist']:
            # Logout any Receptionist currently logged in
            del request.session['user_staff']
        # END: if request.session['user_receptionist']:

        if request.session['user_staff']:
            # Logout any official currently logged in
            del request.session['user_staff']
        # END: if request.session['user_staff']:

        if request.session['current_time']:
            # Delete the current time session
            del request.session['current_time']
        # END: if request.session['current_time']:

        # After logging out any possible user, redirect to login page
        return redirect('systemAdmin:login')
    except KeyError:
        # OTHERWISE. redirect to login page
       return redirect('systemAdmin:login')
    # END OF: try
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
def set_session_data(request, uid):
    if uid:
        u = SystemAdmin.objects.get(system_admin_id=uid)
        request.session['app'] = 'orims.com'
        request.session['user_admin'] = uid

        request.session['username']= u.system_admin_user_name
        request.session['role']= 'Administrator'
        request.session['email']= u.system_admin_email
        request.session['profile_photo'] = u.system_admin_profile_photo.url

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
        request.session['meta'] = meta_data
# End of def set_ssession_data()
