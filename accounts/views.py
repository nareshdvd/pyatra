from django.shortcuts import render, render_to_response
from django.contrib.auth.models import User
from accounts.models import UsageToken
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
import json

from django.views.decorators.csrf import ensure_csrf_cookie
def login(request):
  response_dict = {}
  return render_to_response('accounts/login.html', response_dict, RequestContext(request))

def login_post(request):
  post_data = request.POST.dict()
  email = post_data['email']
  token = post_data['token']
  user = User.objects.filter(email=email).first()
  return_data = {}
  if user is not None:
    usage_token = UsageToken.objects.filter(user=user, token=token).first()
    if usage_token is not None:
      # user details successfully authenticated
      user = authenticate(username=user.username, password=token)
      if user is not None:
        auth_login(request, user)
        return_data = {
          'status' : 'success',
          'message' : 'You are logged in successfully'
        }
  if not return_data:
    return_data = {
      'status' : 'error',
      'message' : 'Invalid credentials'
    }
  return HttpResponse(json.dumps(return_data), content_type = 'application/json')

def logout_post(request):
  auth_logout(request)
  return HttpResponse(json.dumps({'status' : 'success'}), content_type = 'application/json')
