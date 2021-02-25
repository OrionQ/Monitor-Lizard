from django.contrib import admin

from .models import Metric, Host, HostTag, Report, Team, User, AlertRule, Alert

# Registering models for the admin page

admin.site.register(Metric)
admin.site.register(Host)
admin.site.register(HostTag)
admin.site.register(Report)
admin.site.register(Team)
admin.site.register(User)
admin.site.register(AlertRule)
admin.site.register(Alert)
