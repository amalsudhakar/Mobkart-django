from django.shortcuts import redirect, render
from .models import Account
from .forms import RegistrationForm
from django.contrib import messages, auth
from functools import wraps
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required

# verifications

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


def redirect_authenticated_user(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('store')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(
                first_name=first_name, last_name=last_name, email=email, password=password, username=username)
            user.phone_number = phone_number
            user.save()

            messages.success(request, 'Registration Success')
            return redirect('register')
    else:
        form = RegistrationForm()

    context = {'form': form}
    return render(request, 'Accounts/register.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request):
    if 'email' in request.session:
        return redirect('/')
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None and user.is_admin is False:
            auth.login(request, user)
            request.session['email'] = user.email
            request.session['uid'] = user.id
            request.session['first_name'] = user.first_name
            request.session['last_name'] = user.last_name
            messages.success(request, 'You are Logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'invalid login credentials')
            return redirect('login')
    if request.session.get('username'):
        return redirect('store')
    return render(request, 'Accounts/login.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out')
    return redirect('login')


@login_required(login_url = 'login')
def dashboard(request):
    return render(request, 'Accounts/dashboard.html')