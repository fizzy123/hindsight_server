import json
import time
import pdb
import logging
log = logging.getLogger(__name__)

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required

from memories.models import Memory
from general.functions import distance_on_unit_sphere, coordinate_range
from users.models import HindsightUser

def view_near(request):
    if request.META['REQUEST_METHOD'] == 'GET':
        latitude = float(request.GET['latitude'])
        longitude = float(request.GET['longitude'])

        [lat_range, lon_range] = coordinate_range(latitude, longitude, .1)
        memories = Memory.objects.filter(latitude__range = (lat_range[1], lat_range[0])).filter(longitude__range = (lon_range[0], lon_range[1]))
        
        response = {}
        response['memories'] = []
        for memory in memories:
            owned_by_user = False
            user = memory.owner.user
            if request.user.is_authenticated():
                if user == request.user:
                    owned_by_user = True
            
            response['memories'].append({'owner':memory.owner.user.username,'caption':memory.caption,'image':memory.image.name, 'created':memory.created.strftime("%d/%m/%y"), 'id': memory.id, 'owned_by_user':owned_by_user, 'latitude':memory.latitude, 'longitude':memory.longitude})
        response['memories'] = sorted(response['memories'], key=lambda k: time.strptime(k['created'], "%d/%m/%y"))
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        return HttpReponseBadRequest()

def view_owned(request):
    if request.META['REQUEST_METHOD'] == 'GET':
        if request.user.is_authenticated():
            latitude = float(request.GET['latitude'])
            longitude = float(request.GET['longitude'])
            memories = Memory.objects.filter(owner=HindsightUser.objects.get(user=request.user.id))
            response = {}
            response['memories'] = []
            for memory in memories:
                response['memories'].append({'owner':memory.owner.user.username, 'caption':memory.caption, 'image':memory.image.name,'created':memory.created.strftime("%d/%%m/%y"),'id':memory.id, 'latitude':memory.latitude, 'longitude':memory.longitude})
            return HttpResponse(json.dumps(response), content_type="application/json")
        else:
            return HttpResponseForbidden()
    else:
        return HttpReponseBadRequest()

def view_specific(request, memory_id):
    if request.META['REQUEST_METHOD'] == 'GET':
        latitude = float(request.GET['latitude'])
        longitude = float(request.GET['longitude'])
        memory = Memory.objects.get(pk = memory_id)

        owned_by_user = False
        user = memory.owner.user
        if request.user.is_authenticated():
            if user == request.user:
                owned_by_user = True

        response = {}
        response['memory'] = {'owner':memory.owner.user.username, 'caption':memory.caption, 'image':memory.image.name, 'created':memory.created.strftime("%d/%%m/%y"), 'latitude': memory.latitude, 'longitude': memory.longitude, 'owned_by_user': owned_by_user}
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        return HttpReponseBadRequest()

def edit(request, memory_id):
    if request.META['REQUEST_METHOD'] == 'POST':
        memory = Memory.objects.get(pk = memory_id)
        
        user = memory.owner.user
        if request.user.is_authenticated():
            if user == request.user:
                memory.caption = request.POST['caption']
                memory.save()
                return HttpResponse()
        return HttpResponseForbidden()
    return HttpResponseBadRequest()

def delete(request, memory_id):
    if request.META['REQUEST_METHOD'] == 'POST':
        memory = Memory.objects.get(pk = memory_id)

        user = memory.owner.user
        if request.user.is_authenticated():
            if user == request.user:
                memory.delete()
                return HttpResponse()
        return HttpResponseForbidden()
    return HttpResponseBadRequest()

def add(request):
    if request.user.is_authenticated():
        if request.META['REQUEST_METHOD'] == 'POST':
            memory = Memory.objects.get_or_create(image = request.FILES['memory'], owner = HindsightUser.objects.get(user=request.user), latitude = request.POST['latitude'], longitude = request.POST['longitude'])[0]
            if request.POST.has_key('caption'):
                memory.caption = request.POST['caption']
            memory.save()
            return HttpResponse()
        else:
            return HttpReponseBadRequest()
    else:        
        return HttpResponseForbidden()
