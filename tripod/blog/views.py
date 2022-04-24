from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from blog.forms import CustomerCreationForm


def registerPage(request):
    """
    Account registration view function for customers or users
    using email, username and password
    """
    # if request.user.is_authenticated:
    #     return redirect('core:home')
    # else:
    form = CustomerCreationForm()
    if request.method == "POST":
        form = CustomerCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('email')
            messages.success(request, f'Account was created for {user}')
            return redirect('core:login')
        else:
            print(form.errors)

    context = {'form': form}
    return render(request, 'main/register.html', context)
