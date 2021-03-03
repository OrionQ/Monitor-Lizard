from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Host)
admin.site.register(Metric)
admin.site.register(HostTag)
admin.site.register(Report)
admin.site.register(Team)
admin.site.register(User)
admin.site.register(AlertRule)
admin.site.register(Alert)