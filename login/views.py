from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def login(request):
    return render(request,"login.html")

@csrf_exempt 
def submit_login(request):
    """User Authentication"""
    email=request.POST.get('email')
    password=request.POST.get('password')
    username = User.objects.get(email=email.lower()).username
    user = authenticate(request, username=username, password=password)

    if user is not None:
        auth_login(request,user)
        return redirect('tasks:main')
    else:
        print('warn')

    return render(request,"login.html")

@csrf_exempt 
def submit_register(request):
    """User Registration"""
    name=request.POST.get('name')
    email=request.POST.get('email')
    password=request.POST.get('password')
    
    name=name.upper()
    user = User.objects.create_user(name, email, password)
    user.save()

    return render(request,"login.html")