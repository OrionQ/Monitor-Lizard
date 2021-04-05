from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from web.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
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

@login_required(login_url='login')
def home(request):
    report_list = Report.objects.all()
    tag_list = HostTag.objects.all()
    for val in tag_list:
        host_list = val.hosts.count()

    paginator = Paginator(report_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Returning a template
    return render(request, 'web/dashboard.html', {'page_obj': page_obj, 'tag_list': tag_list, 'host_list': host_list})

@login_required(login_url='login')
def tag(request, tag_test):
    tag = HostTag.objects.get(name=tag_test)
    host_list = tag.hosts.all()
    for val in host_list:
        report_list = Report.objects.filter(host=val)
        report_count = report_list.count()
        last_report = Report.objects.filter(host=val).last()
        last_timestamp = last_report.time

        last_four = Report.objects.filter(host=val)[:4]
        times = []
        for val in last_four:
            # times.append(val.value)
            if val.metric.name == 'ram_usage':
                ram_usage = val.value
            if val.metric.name == 'cpu_temperature':
                cpu_temperature = val.value
            if val.metric.name == 'disk_usage':
                disk_usage = val.value
            if val.metric.name == 'cpu_usage':
                cpu_usage = val.value
    return render(request, 'web/tag.html', {'host_list': host_list, 'report_count': report_count, 
                    'last_timestamp': last_timestamp, 'tag_test': tag_test, 'ram_usage': ram_usage, 
                    'cpu_usage': cpu_usage, 'disk_usage': disk_usage, 'cpu_temperature': cpu_temperature})

@login_required(login_url='login')
def host(request, host_test):
    host = Host.objects.get(guid=host_test)
    return render(request, 'web/host.html', {'host_test': host_test})

@login_required(login_url='login')
def containers(request):
    return render(request, 'web/containers.html')

@login_required(login_url='login')
def processes(request):
    return render(request, 'web/processes.html')