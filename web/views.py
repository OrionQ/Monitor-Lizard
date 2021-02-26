from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    # Returning a template
    return render(request, 'web/dashboard.html')

def tag(request):
    return render(request, 'web/tag.html')

def host(request):
    return render(request, 'web/host.html')