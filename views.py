import json
import re
from string import rstrip
from urlparse import urljoin
from django.shortcuts import render, HttpResponse
from cartoview.app_manager.models import App, AppInstance
from django.conf import settings
from . import APP_NAME
from django.contrib.auth.decorators import login_required

VIEW_TPL = "%s/index.html" % APP_NAME
NEW_EDIT_TPL = "%s/new.html" % APP_NAME


def view(request, resource_id):
    instance = AppInstance.objects.get(pk=resource_id)
    context = dict(instance=instance)
    return render(request, VIEW_TPL, context)


def save(request, instance_id=None):
    res = dict(success=False, errors=dict())
    config_str = request.POST.get('config', None)
    config = json.loads(config_str)
    title = config['title']
    abstract = "" if 'summary' not in config else config['summary']
    required_fields = {
        'webmap': "Please Choose a webmap",
        'title': 'Please Enter a valid title'
    }
    valid = True
    for f in required_fields.keys():
        val = config.get(f, "").strip()
        if val == "":
            res["errors"][f] = required_fields[f]
            valid = False
    if valid:
        if instance_id is None:
            instance_obj = AppInstance()
            instance_obj.app = App.objects.get(name=APP_NAME)
            instance_obj.owner = request.user
        else:
            instance_obj = AppInstance.objects.get(pk=instance_id)
        instance_obj.title = title
        instance_obj.config = config_str
        instance_obj.abstract = abstract
        instance_obj.save()
        res.update(dict(success=True, id=instance_obj.id))
    return HttpResponse(json.dumps(res), content_type="text/json")

@login_required
def new(request):
    if request.method == 'POST':
        return save(request)
    context = {}
    return render(request, NEW_EDIT_TPL, context)

@login_required
def edit(request, resource_id):
    if request.method == 'POST':
        return save(request, resource_id)
    instance = AppInstance.objects.get(pk=resource_id)
    context = dict(instance=instance)
    return render(request, NEW_EDIT_TPL, context)


import requests
def proxy(request):
    params = []
    keys = ["http://live.esri.com/LiveMaps/feed.php?feed", "keyword", "lat","lon", "radius", "bbox"]
    for key in keys:
        val = request.GET.get(key, None)
        if val is not None:
            params.append("%s=%s" % (key, val))
    url = "&".join(params)
    return HttpResponse(requests.get(url).text, content_type="text/json")
