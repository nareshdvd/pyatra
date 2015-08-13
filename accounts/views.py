from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from lib.decorators import *
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from lib.validators import FormValidator
from lib.classes import *
from accounts.models import UsageToken

@flashable
@anonymous_only
def signin(request):
  try:
    flash_data = request.flash_data
    form = request.form
  except:
    flash_data = {}
    form = {}
  response_dict = {
    'flash_data' : flash_data,
    'form' : form
  }

  return render_to_response('accounts/signin.html', response_dict, RequestContext(request))

@post
@anonymous_only
def signin_post(request):
  post_data = request.POST.dict()
  email = post_data['email']
  token = post_data['token']
  usage_token = UsageToken.objects.filter(email=email, token=token, used=False).first()
  if usage_token is not None:
    user = User.objects.filter(email=email).first()
    if user is None:
      username = email.split("@")[0]
      user = User.objects.create_user(username=username, email=email, password=token)
    else:
      username = user.username
    print username
    print token
    user = authenticate(username=username, password=token)
    if user is not None:
      login(request, user)
      request.session['usage_token'] = usage_token.token
      flash_data = {
        'status' : 'success',
        'message' : 'You are logged in successfully'
      }
      redirect_url = '/yatra/categories'
  else:
    flash_data = {
      'status' : 'error',
      'message' : 'Invalid Token'
    }
    redirect_url = '/accounts/signin'
  return FlashedRedirect(redirect_url, request, flash_data, post_data)





@token_user_only
def signout(request):
  try:
    del request.session['usage_token']
  except:
    pass
  logout(request)
  flash_data = {
    'status' : 'success',
    'message' : 'You are successfully signed out'
  }
  return FlashedRedirect('/accounts/signin', request, flash_data)
