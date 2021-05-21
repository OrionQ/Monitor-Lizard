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
    # To get the list of metrics being queried
    metric_names = Metric.objects.values_list('name', flat=True)

    tag_list = HostTag.objects.all()
    for val in tag_list:
        # To get the number of hosts in the tag
        host_list = val.hosts.count()

    alert_list = Alert.objects.all()
    alert_labels = []
    alert_data = []
    # Key value pairs of tag name : number of alerts
    # This is used for the alerts by tag chart
    alert_dict = {}
    for val in alert_list:
        if val.host_tag.name not in alert_dict:
            alert_dict[val.host_tag.name] = 1
        else:
            alert_dict[val.host_tag.name] += 1
    for key, val in alert_dict.items():
        # Labels are the tag names
        alert_labels.append(key)
        # Data is the number of alerts for each tag
        alert_data.append(val)

    # Pagination for the reports table
    paginator = Paginator(report_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Returning a template
    return render(request, 'web/dashboard.html', {'page_obj': page_obj, 'tag_list': tag_list, 'host_list': host_list,
                                                  'metric_names': metric_names, 'alert_labels': alert_labels, 'alert_data': alert_data,
                                                  'alert_list': alert_list})


@login_required(login_url='login')
def tag(request, tag_id):
    tag = HostTag.objects.get(name=tag_id)
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

        # 3. Get the last recorded values of the metrics
        if Report.objects.filter(host__guid=val.guid, metric__name='ram_usage').last() is not None:
            ram_usage = Report.objects.filter(host__guid=val.guid,
                                              metric__name='ram_usage').last().value
        else:
            ram_usage = "N/A"
        if Report.objects.filter(host__guid=val.guid, metric__name='disk_usage').last() is not None:
            disk_usage = Report.objects.filter(host__guid=val.guid,
                                               metric__name='disk_usage').last().value
        else:
            disk_usage = "N/A"
        if Report.objects.filter(host__guid=val.guid, metric__name='cpu_usage').last() is not None:
            cpu_usage = Report.objects.filter(host__guid=val.guid,
                                              metric__name='cpu_usage').last().value
        else:
            cpu_usage = "N/A"
        if Report.objects.filter(host__guid=val.guid, metric__name='cpu_temperature').last() is not None:
            cpu_temperature = Report.objects.filter(host__guid=val.guid,
                                                    metric__name='cpu_temperature').last().value
        else:
            cpu_temperature = "N/A"

    return render(request, 'web/tag.html', {'host_list': host_list, 'report_count': report_count,
                                            'last_timestamp': last_timestamp, 'tag_test': tag_id, 'ram_usage': ram_usage,
                                            'cpu_usage': cpu_usage, 'disk_usage': disk_usage, 'cpu_temperature': cpu_temperature})


@login_required(login_url='login')
def host(request, host_id):
    host = Host.objects.get(guid=host_id)

    # Labels & data for RAM Usage chart
    ram_labels = []
    ram_data = []
    ram_reports = Report.objects.filter(
        host__guid=host_id, metric__name='ram_usage')
    for val in ram_reports:
        # Labels for RAM usage chart are the timestamps
        ram_labels.append(val.time)
        # Values for RAM usage chart are the metric values
        ram_data.append(val.value)

    # Labels & data for the CPU Usage chart
    cpu_labels = []
    cpu_data = []
    cpu_reports = Report.objects.filter(
        host__guid=host_id, metric__name='cpu_usage')
    for val in cpu_reports:
        # Labels for CPU usage chart are the timestamps
        cpu_labels.append(val.time)
        # Values for CPU usage chart are the metric values
        cpu_data.append(val.value)

    # Labels & data for the Disk Usage chart
    disk_labels = []
    disk_data = []
    disk_reports = Report.objects.filter(
        host__guid=host_id, metric__name='disk_usage')
    for val in disk_reports:
        # Labels for Disk usage chart are the timestamps
        disk_labels.append(val.time)
        # Labels for Disk usage chart are the metric values
        disk_data.append(val.value)

    # Labels & data for the CPU Temperature chart
    cpu_temp_labels = []
    cpu_temp_data = []
    cpu_temp_reports = Report.objects.filter(
        host__guid=host_id, metric__name='cpu_temperature')
    for val in cpu_temp_reports:
        # Labels for CPU temperature chart are the timestamps
        cpu_temp_labels.append(val.time)
        # Labels for CPU temperature chart are the metric values
        cpu_temp_data.append(val.value)

    last_report = Report.objects.filter(host__guid=host_id).last()
    if last_report is not None:
        last_timestamp = last_report.time
    else:
        last_timestamp = "N/A"

    # These values are to be used in the large boxes
    # at the top of the host page
    ram_usage = host.get_metric('ram_usage')
    if ram_usage is not None:
        # Querysets for Lowest and Highest RAM Usage values
        ram_usage_query = Report.objects.filter(
            host=host, metric__name='ram_usage').order_by('value')
        least_ram_usage = ram_usage_query.first().value
        most_ram_usage = ram_usage_query.last().value
    else:
        ram_usage = "N/A"
        least_ram_usage = "N/A"
        most_ram_usage = "N/A"

    disk_usage = host.get_metric('disk_usage')
    if disk_usage is not None:
        # Querysets for Lowest and Highest Disk Usage values
        disk_usage_query = Report.objects.filter(
            host=host, metric__name='disk_usage').order_by('value')
        least_disk_usage = disk_usage_query.first().value
        most_disk_usage = disk_usage_query.last().value
    else:
        disk_usage = "N/A"
        least_disk_usage = "N/A"
        most_disk_usage = "N/A"

    cpu_usage = host.get_metric('cpu_usage')
    if cpu_usage is not None:
        # Querysets for Lowest and Highest CPU Usage values
        cpu_usage_query = Report.objects.filter(
            host=host, metric__name='cpu_usage').order_by('value')
        least_cpu_usage = cpu_usage_query.first().value
        most_cpu_usage = cpu_usage_query.last().value
    else:
        cpu_usage = "N/A"
        least_cpu_usage = "N/A"
        most_cpu_usage = "N/A"

    cpu_temperature = host.get_metric('cpu_temperature')
    if cpu_temperature is not None:
        # Querysets for Lowest and Highest CPU Temperature values
        cpu_temperature_query = Report.objects.filter(
            host=host, metric__name='cpu_temperature').order_by('value')
        least_cpu_temperature = cpu_temperature_query.first().value
        most_cpu_temperature = cpu_temperature_query.last().value
    else:
        cpu_temperature = "N/A"
        least_cpu_temperature = "N/A"
        most_cpu_temperature = "N/A"

    return render(request,
                  'web/host.html',
                  {'host_test': host_id, 'ram_usage': ram_usage, 'cpu_usage': cpu_usage,
                   'disk_usage': disk_usage, 'cpu_temperature': cpu_temperature,
                   'least_ram_usage': least_ram_usage, 'most_ram_usage': most_ram_usage,
                   'last_timestamp': last_timestamp, 'least_cpu_usage': least_cpu_usage,
                   'most_cpu_usage': most_cpu_usage, 'least_disk_usage': least_disk_usage,
                   'most_disk_usage': most_disk_usage, 'least_cpu_temperature': least_cpu_temperature,
                   'most_cpu_temperature': most_cpu_temperature, 'host_tags': HostTag.objects.filter(hosts=host),
                   'ram_labels': ram_labels, 'ram_data': ram_data, 'cpu_labels': cpu_labels,
                   'cpu_data': cpu_data, 'disk_labels': disk_labels, 'disk_data': disk_data,
                   'cpu_temp_labels': cpu_temp_labels, 'cpu_temp_data': cpu_temp_data, 'metrics': Metric.objects.all(), 'chartable_metrics': ['Integer', 'Floating point']})


@login_required(login_url='login')
def containers(request, host_id):
    host = Host.objects.get(guid=host_id)
    return render(request, 'web/containers.html', {'host': host})


@login_required(login_url='login')
def processes(request, host_id):
    host = Host.objects.get(guid=host_id)
    return render(request, 'web/processes.html', {'host': host})
