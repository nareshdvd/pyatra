from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from lib.decorators import *
from lib.validators import FormValidator
from lib.classes import FlashedRedirect
from accounts.models import UsageToken

@admin_only
@flashable
def index(request):
  usage_tokens = UsageToken.unused()
  response_dict = {
    'usage_tokens' : usage_tokens
  }
  try:
    response_dict['flash_data'] = request.flash_data
  except:
    pass
  return render_to_response('admins/usage_tokens/index.html', response_dict, RequestContext(request))


@admin_only
@flashable
def new(request):
  response_dict = {}
  try:
    response_dict['flash_data'] = request.flash_data
    response_dict['form'] = request.form
  except:
    pass
  return render_to_response('admins/usage_tokens/new.html', response_dict, RequestContext(request))


@admin_only
@post
def save(request):
  post_data = request.POST.dict()
  validator = FormValidator(post_data, {
    'email' : 'is_email'
  })
  validator.validate()
  flash_data = {}
  if validator.has_errors():
    errors = validator.get_errors()
    flash_data = {
      'status' : 'error',
      'message' : 'Form contains errors',
      'errors' : errors
    }
    response = FlashedRedirect('/admins/usage_tokens/new', request, flash_data, post_data)
  else:
    utoken = UsageToken.generate(post_data['email'])
    flash_data = {
      'status' : 'success',
      'message' : 'Token Generated successfully: {}'.format(utoken.token)
    }
    response = FlashedRedirect('/admins/usage_tokens', request, flash_data)
  return response

def edit(request, id):
  pass

def update(request, id):
  pass

@admin_only
def delete(request, id):
  try:
    UsageToken.objects.get(pk=id).delete()
    flash_data = {
      'status' : 'success',
      'message' : 'Token deleted successfully'
    }
  except:
    flash_data = {
      'status' : 'success',
      'message' : 'Token not found'
    }
  return FlashedRedirect('/admins/usage_tokens', request, flash_data)