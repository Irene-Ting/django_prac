from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import auth
from user.forms import UserCreationForm
from django.contrib.auth.models import User, Group, Permission

def index(request):
    return render(request, 'index.html', locals())


def redirect(request):
    return HttpResponseRedirect('/index/')


def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/index/')
    
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    user = auth.authenticate(username=username, password=password)

    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect('/index/')
    else:
        return render(request, 'login.html', locals())


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/index/')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect('/accounts/login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', locals())