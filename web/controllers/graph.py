
from web.models import Host, Metric, Report
from datetime import datetime, timedelta
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


@login_required(login_url='login')
@require_GET
def host_metric(request, host_id, metric_name):
    host = Host.objects.get(guid=host_id)
    metric = Metric.objects.get(name=metric_name)

    if 'end' in request.GET:
        end_date = datetime.fromisoformat(request.GET['end'])
    else:
        end_date = datetime.now()
    if 'count' in request.GET:
        count = int(request.GET['count'])
    else:
        count = 100

    # Labels & data for the chart
    labels = []
    data = []
    # 100 most recent reports before the end date
    reports = Report.objects.filter(
        host=host, metric__name=metric_name, time__lt=end_date).order_by('-time')[:count]
    for report in reports:
        # Labels for CPU temperature chart are the timestamps
        labels.append(report.time)
        # Labels for CPU temperature chart are the metric values
        data.append(report.value)
    return JsonResponse(data={'labels': labels, 'data': data})
