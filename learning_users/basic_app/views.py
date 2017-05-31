from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm


#
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request,'basic_app/index.html')

# the login_required decorator means the function is only available
# if the user is logged in! Thanks Django!
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index.html'))

@login_required
def special(request):
    # Remember to also set login url in settings.py!
    # LOGIN_URL = '/basic_app/user_login/'
    return HttpResponse("You are logged in. Nice!")

def register(request):

    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            # this set_password method is how we hash the password
            user.save()
            # you must save the user model before you can create a UserProfileInfo record

            profile = profile_form.save(commit=False)
            # Here we set commit to False so django doesn't try to
            # save the data to the db before we've worked on it
            profile.user = user
            # user in form = user in module

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else: # if request was just http then display form
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'basic_app/registration.html',
                        {'user_form':user_form,
                        'profile_form':profile_form,
                        'registered':registered})
    # this is where we set up the context dictionary to link
    # the variables to the template tags


def user_login(request):
    # don't call a view anything you're importing above like 'login'
    if request.method == 'POST':
        # (user has filled in login form)
        username = request.POST.get('username')
        # Get username and password
        # get('username') grabs the input from the html tag named 'username'
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)
        # This code will authenticate the user for you, thanks Django!

        if user:
            # if authenticated
            if user.is_active:
                # if active
                login(request,user)
                # Django's login function
                return HttpResponseRedirect(reverse('index'))
                # return to homepage
            else:
                return HttpResponse("Account Not Active")
        else:
            print('Someone tried to log in and failed')
            print("Username: {} and password: {}".format(username,password))
            # printing to the console the incorrect details for you to see
            return HttpResponse('invalid username or password')
    else:
        # request not equal to POST
        return render(request,'basic_app/login.html',{})
