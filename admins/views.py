from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from lib.decorators import *
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from accounts.models import *
from yatra.models import *
from lib.validators import FormValidator
from lib.classes import *


@anonymous_only
@flashable
def signin(request):
  response_dict = {}
  try:
    response_dict['flash_data'] = request.flash_data
  except:
    pass
  response = render_to_response('admins/signin.html', response_dict, RequestContext(request))
  return response


@anonymous_only
@post
def signin_post(request):
  data = request.POST.dict()
  email = data['email']
  password = data['password']
  user = User.objects.filter(email=email).first()
  has_error = False
  if user is not None:
    username = user.username
    user = authenticate(username=username, password=password)
    if user is not None:
      if user.is_superuser:
        if user.is_active:
          login(request, user)
          flash_data = {
            'status' : 'success',
            'message' : 'You are successfully logged in'
          }
          redirect_url = reverse('admins:dashboard')
        else:
          has_error = True
          flash_data = {
            'status' : 'error',
            'message' : 'Inactive user'
          }
          redirect_url = reverse('admins:signin')
      else:
        has_error = True
        flash_data = {
          'status' : 'error',
          'message' : 'Admin access only'
        }
        redirect_url = reverse('admins:signin')
    else:
      has_error = True
      flash_data = {
        'status' : 'error',
        'message' : 'Incorrect credentials'
      }
      redirect_url = reverse('admins:signin')
  else:
    has_error = True
    flash_data = {
      'status' : 'error',
      'message' : 'Incorrect credentials'
    }
    redirect_url = reverse('admins:signin')
  return FlashedRedirect(redirect_url, request, flash_data, {})

@admin_only
def signout(request):
  logout(request)
  return HttpResponseRedirect(reverse('admins:signin'))

@admin_only
@flashable
def dashboard(request):
  response_dict = {}
  try:
    response_dict['flash_data'] = request.flash_data
  except:
    pass
  return render_to_response('admins/dashboard.html', response_dict, RequestContext(request))