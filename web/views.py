from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def loginPage(request):
    if request.method == 'POST':
        # Grab the username and password
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        # Log the user in
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "Incorrect Credentials")
    context = {}
    return render(request, 'web/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def home(request):
    # Returning a template
    return render(request, 'web/dashboard.html')

def tag(request):
    return render(request, 'web/tag.html')

def host(request):
    return render(request, 'web/host.html')