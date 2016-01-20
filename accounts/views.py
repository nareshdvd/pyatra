from django.shortcuts import render, render_to_response
from django.contrib.auth.models import User
from accounts.models import UsageToken
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponseRedirect
from django.template import RequestContext
def login(request):
  response_dict = {}
  return render_to_response('accounts/login.html', response_dict, RequestContext(request))

def login_post(request):
  post_data = request.POST.dict()
  email = post_data['email']
  token = post_data['token']
  user = User.objects.filter(email=email)
  if user is not None:
    usage_token = UsageToken.objects.filter(user=user, token=token, used=False).first()
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
      redirect_url = '/accounts/login'
  else:
    flash_data = {
      'status' : 'error',
      'message' : 'Invalid Token'
    }
    redirect_url = '/accounts/login'
  return FlashedRedirect(redirect_url, request, flash_data, post_data) 