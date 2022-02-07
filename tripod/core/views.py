from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from core.forms import (
    CustomUserCreationForm,
    )


def registerPage(request):
    """
    Account registration view function for customers or users
    using email, username and password
    """
    if request.user.is_authenticated:
        return redirect('core:home')
    else:
        form = CustomUserCreationForm()
        if request.method == "POST":
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('email')
                messages.success(request, f'Account was created for {user}')
                return redirect('core:login')

        context = {'form': form}
        return render(request, 'accounts/register.html', context)


def loginPage(request):
    """
    Login view function for customers or users using email and password
    """
    if request.user.is_authenticated:
        return redirect('core:home')
    else:
        if request.method == "POST":
            email = request.POST.get('email')
            password = request.POST.get('password')

            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('core:home')
            else:
                messages.info(request, 'Username or password incorrect')

        context = {}
        return render(request, 'accounts/login.html', context)


@login_required(login_url='core:login')
def logoutPage(request):
    """
    Logout view function for customers or user
    which redirects back to home
    """
    logout(request)
    return redirect('core:login')


def home(request):
    """
    customers or users home view function
    """
    context = {}
    context['user'] = request.user
    return render(request, 'accounts/home.html', context)
