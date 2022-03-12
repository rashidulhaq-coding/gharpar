from .models import *
from django.shortcuts import render, redirect
from django.contrib import messages
# restricting user to access only their own data using decorators

def only_admin(function):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return function(request, *args, **kwargs)
            else:
                messages.error(request, 'You are not authorized to access this page')
                return redirect('/')
        else:
            messages.error(request, 'You are not authorized to access this page, please login!')
            return redirect('login')
    return wrapper

def only_employee(function):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_employee:
                return function(request, *args, **kwargs)
            else:
                return redirect('/')
        else:
            return redirect('login')
    return wrapper

def only_user(function):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_employee == False and request.user.is_superuser == False:
            return function(request, *args, **kwargs)
        else:
            return redirect('/')
    return wrapper
