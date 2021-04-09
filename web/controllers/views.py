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

    # Pagination for the reports table
    paginator = Paginator(report_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Returning a template
    return render(request, 'web/dashboard.html', {'page_obj': page_obj, 'tag_list': tag_list, 'host_list': host_list})

@login_required(login_url='login')
def tag(request, tag_test):
    tag = HostTag.objects.get(name=tag_test)
    host_list = tag.hosts.all()
    # For each host in the tag
    for val in host_list:
        report_list = Report.objects.filter(host=val)
        # 1. Get the number of reports generated
        report_count = report_list.count()
        last_report = Report.objects.filter(host=val).last()
        # 2. The timestamp of the last report generated
        if last_report is not None:
            last_timestamp = last_report.time
        else:
            # Error handling in case there are no reports
                # currently in the database
            last_timestamp = "N/A"

        # Getting the last four reports generated
        last_four = Report.objects.filter(host=val)[:4]
        # Setting the initial values of the metrics
        ram_usage = "N/A"
        cpu_usage = "N/A"
        disk_usage = "N/A"
        cpu_temperature = "N/A"
        # 3. Get the last recorded values of the metrics
        for val in last_four:
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

    # Labels & data for RAM Usage chart
    ram_labels = []
    ram_data = []
    ram_reports = Report.objects.filter(host__guid=host_test).filter(metric__name='ram_usage')
    for val in ram_reports:
        # Labels for RAM usage chart are the timestamps
        ram_labels.append(val.time)
    for val_two in ram_reports:
        # Values for RAM usage chart are the metric values
        ram_data.append(val_two.value)

    # Labels & data for the CPU Usage chart
    cpu_labels = []
    cpu_data = []
    cpu_reports = Report.objects.filter(host__guid=host_test).filter(metric__name='cpu_usage')
    for val in cpu_reports:
        # Labels for CPU usage chart are the timestamps
        cpu_labels.append(val.time)
    for val_two in cpu_reports:
        # Values for CPU usage chart are the metric values
        cpu_data.append(val_two.value)

    # Labels & data for the Disk Usage chart
    disk_labels = []
    disk_data = []
    disk_reports = Report.objects.filter(host__guid=host_test).filter(metric__name='disk_usage')
    for val in disk_reports:
        # Labels for Disk usage chart are the timestamps
        disk_labels.append(val.time)
    for val_two in disk_reports:
        # Labels for Disk usage chart are the metric values
        disk_data.append(val_two.value)

    # Labels & data for the CPU Temperature chart
    cpu_temp_labels = []
    cpu_temp_data = []
    cpu_temp_reports = Report.objects.filter(host__guid=host_test).filter(metric__name='cpu_temperature')
    for val in cpu_temp_reports:
        # Labels for CPU temperature chart are the timestamps
        cpu_temp_labels.append(val.time)
    for val_two in cpu_temp_reports:
        # Labels for CPU temperature chart are the metric values
        cpu_temp_data.append(val_two.value)

    last_four = Report.objects.filter(host__guid=host_test)[:4]
    tags = HostTag.objects.all()
    host_tags = []
    # For loop to iterate over all of the tags
    for val in tags.all():
        # For loop to iterate over all the hosts in the tag
        for host_val in val.hosts.all():
            # Check if the host whose page we're currently on
                # is present in this tag
            if str(host_val.guid) == host_test:
                # If it is present, add the tag to the list
                    # of tags associated with this host
                host_tags.append(val.name)

    last_report = Report.objects.filter(host__guid=host_test).last()
    if last_report is not None:
        last_timestamp = last_report.time
    else:
        last_timestamp = "N/A"
    
    # These values are to be used in the large boxes
        # at the top of the host page
    ram_usage = "N/A"
    cpu_usage = "N/A"
    disk_usage = "N/A"
    cpu_temperature = "N/A"
    for val in last_four:
        if val.metric.name == 'ram_usage':
            ram_usage = val.value
        if val.metric.name == 'cpu_temperature':
            cpu_temperature = val.value
        if val.metric.name == 'disk_usage':
            disk_usage = val.value
        if val.metric.name == 'cpu_usage':
            cpu_usage = val.value

    # Querysets for Lowest and Highest RAM Usage values
    if Report.objects.filter(host__guid=host_test).filter(metric__name='ram_usage').order_by('value').first() is not None:
        least_ram_usage = Report.objects.filter(host__guid=host_test).filter(metric__name='ram_usage').order_by('value').first().value
        most_ram_usage = Report.objects.filter(host__guid=host_test).filter(metric__name='ram_usage').order_by('value').last().value
    else:
        # Error checking for if there are no reports in the database
        least_ram_usage = "N/A"
        most_ram_usage = "N/A"
    # Querysets for Lowest and Highest CPU Usage values
    if Report.objects.filter(host__guid=host_test).filter(metric__name='cpu_usage').order_by('value').first() is not None:
        least_cpu_usage = Report.objects.filter(host__guid=host_test).filter(metric__name='cpu_usage').order_by('value').first().value
        most_cpu_usage = Report.objects.filter(host__guid=host_test).filter(metric__name='cpu_usage').order_by('value').last().value
    else:
        # Error checking for if there are no reports in the database
        least_cpu_usage = "N/A"
        most_cpu_usage = "N/A"
    # Querysets for Lowest and Highest Disk Usage values
    if Report.objects.filter(host__guid=host_test).filter(metric__name='disk_usage').order_by('value').first() is not None:
        least_disk_usage = Report.objects.filter(host__guid=host_test).filter(metric__name='disk_usage').order_by('value').first().value
        most_disk_usage = Report.objects.filter(host__guid=host_test).filter(metric__name='disk_usage').order_by('value').last().value
    else:
        # Error checking for if there are no reports in the database
        least_disk_usage = "N/A"
        most_disk_usage = "N/A"
    # Querysets for Lowest and Highest CPU Temperature values
    if Report.objects.filter(host__guid=host_test).filter(metric__name='cpu_temperature').order_by('value').first() is not None:
        least_cpu_temperature = Report.objects.filter(host__guid=host_test).filter(metric__name='cpu_temperature').order_by('value').first().value
        most_cpu_temperature = Report.objects.filter(host__guid=host_test).filter(metric__name='cpu_temperature').order_by('value').last().value
    else:
        # Error checking for if there are no reports in the database
        least_cpu_temperature = "N/A"
        most_cpu_temperature = "N/A"

    return render(request, 'web/host.html', {'host_test': host_test, 'ram_usage': ram_usage, 'cpu_usage': cpu_usage, 
                                                'disk_usage': disk_usage, 'cpu_temperature': cpu_temperature, 
                                                'least_ram_usage': least_ram_usage, 'most_ram_usage': most_ram_usage, 
                                                'last_timestamp': last_timestamp, 'least_cpu_usage': least_cpu_usage, 
                                                'most_cpu_usage': most_cpu_usage, 'least_disk_usage': least_disk_usage, 
                                                'most_disk_usage': most_disk_usage, 'least_cpu_temperature': least_cpu_temperature, 
                                                'most_cpu_temperature': most_cpu_temperature, 'host_tags': host_tags, 
                                                'ram_labels': ram_labels, 'ram_data': ram_data, 'cpu_labels': cpu_labels, 
                                                'cpu_data': cpu_data, 'disk_labels': disk_labels, 'disk_data': disk_data, 
                                                'cpu_temp_labels': cpu_temp_labels, 'cpu_temp_data': cpu_temp_data})

@login_required(login_url='login')
def containers(request):
    return render(request, 'web/containers.html')

@login_required(login_url='login')
def processes(request):
    return render(request, 'web/processes.html')