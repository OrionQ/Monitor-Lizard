from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
from django.contrib import messages
from web.models import HostTag, Host
from uuid import uuid4
from django.views.decorators.csrf import csrf_exempt

# Endpoints the host will hit


@csrf_exempt
def register(request):
    if request.method == 'POST':
        # Grab the optional registration_key
        registration_key = request.POST.get('registration_key', default=None)
        if registration_key is not None:
            try:
                tag = HostTag.objects.get(registration_key=registration_key)
            except HostTag.DoesNotExist:
                return HttpResponseBadRequest
        else:
            tag = HostTag.objects.get(name='Unsorted')

        guid = uuid4()
        #name = request.META.get('REMOTE_ADDR')
        tag.hosts.create(guid=guid)
        return JsonResponse({'guid': guid})
    else:
        return HttpResponseNotFound
