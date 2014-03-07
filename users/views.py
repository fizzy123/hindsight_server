import json
import pdb
import logging
log = logging.getLogger(__name__)
import random, string

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required

from users.models import HindsightUser
from general.functions import email

def provide_csrf(request):
    return render(request, 'users/csrf.html')

def user_login(request):
    if request.META['REQUEST_METHOD'] == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user:
            if user.is_active:
                login(request, user)
                response = {'username':user.username}
                return HttpResponse(json.dumps(response),content_type="application/json")
            else:
                return HttpResponseForbidden("NOT_ACTIVE")
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseBadRequest()

def user_logout(request):
    if request.META['REQUEST_METHOD'] == 'POST':
        if request.user.is_authenticated():
            logout(request)
            return HttpResponse()
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseBadRequest()

def verify_email(request, key):
    if request.META['REQUEST_METHOD'] == 'GET':
        h_user = HindsightUser.objects.get(key = key)
        if h_user:
            user = h_user.user
            user.is_active = True
            h_user.key = ''
            h_user.save()
            user.save()
            return HttpResponse("Thank you for confirming your email. You should now be able to log in")
        else: 
            return HttpResponseNotFound()
    else:
        return HttpResponseBadRequest()

def create(request):
    if request.META['REQUEST_METHOD'] == 'POST':
        user = User.objects.all().filter(email=request.POST['email'])
        if user:
            return HttpResponseForbidden("EMAIL_TAKEN")
        user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
        if user:
#            user.is_active = False
            user.save()
            h_user = HindsightUser.objects.create(user=user)
            h_user.key = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for x in range(200))
            h_user.save()
 #           context = {'email':user.email,'key':h_user.key}
 #           email(user.email, 'users/verify_email.html', context)
            return HttpResponse()
        else:
            HttpResponseForbidden("USERNAME_TAKEN")
    else:
        return HttpResponseBadRequest()

def verify(request):
    response = {}
    if request.user.is_authenticated():
        response = {'username':request.user.username}
        return HttpResponse(json.dumps(response),content_type="application/json")
    else:
        return HttpResponseForbidden()    
