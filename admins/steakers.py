from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from lib.decorators import *
from lib.validators import FormValidator
from yatra.models import Steaker
from django.forms.models import model_to_dict
from lib.classes import JsonResponse

def index(request):
  steakers = Steaker.objects.all()
  response_dict = {}
  try:
    response_dict['flash_data'] = request.flash_data
  except:
    pass
  response_dict['steakers'] = steakers
  return render_to_response('admins/steakers/index.html', response_dict, RequestContext(request))

def new(request):
  response_dict = {}
  try:
    response_dict['flash_data'] = request.flash_data
    response_dict['form'] = request.form
  except:
    pass
  return render_to_response('admins/steakers/new.html', response_dict, RequestContext(request))

def save(request):
  post_data = request.POST.dict()
  post_data['image'] = ''
  files_data = request.FILES.dict()
  if 'image' in request.FILES:
    post_data['image'] = request.FILES['image']

  validator = FormValidator(post_data, {
    'image' : 'is_image'
  })
  validator.validate()

  if validator.has_errors():
    errors = validator.get_errors()
    flash_data = {
      'status' : 'error',
      'message' : 'Form contains errors',
      'errors' : errors
    }
    response = FlashedRedirect('/admins/steakers/new', request, flash_data, post_data)
  else:
    steaker = Steaker(**post_data)
    steaker.save()
    flash_data = {
      'status' : 'success',
      'message' : 'Steaker created successfully'
    }
    response = FlashedRedirect('/admins/steakers', request, flash_data)
  return response

def edit(request, id):
  pass

def update(request, id):
  pass

def delete(request):
  pass