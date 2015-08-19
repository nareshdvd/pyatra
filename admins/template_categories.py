from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from lib.decorators import *
from lib.validators import FormValidator
from lib.classes import FlashedRedirect
from accounts.models import UsageToken
from yatra.models import VideoTemplateCategory

@admin_only
@flashable
def index(request):
  template_categories = VideoTemplateCategory.objects.all()
  response_dict = {
    'template_categories' : template_categories
  }
  try:
    response_dict['flash_data'] = request.flash_data
  except:
    pass
  return render_to_response('admins/template_categories/index.html', response_dict, RequestContext(request))

@admin_only
@flashable
def new(request):
  response_dict = {}
  try:
    response_dict['flash_data'] = request.flash_data
    response_dict['form'] = request.form
  except:
    pass
  return render_to_response('admins/template_categories/new.html', response_dict, RequestContext(request))

@admin_only
@post
def save(request):
  post_data = request.POST.dict()
  post_data['cover_image'] = ''
  files_data = request.FILES.dict()
  if 'cover_image' in request.FILES:
    post_data['cover_image'] = request.FILES['cover_image']
  validator = FormValidator(post_data, {
    'title' : 'is_not_empty',
    'description' : 'is_not_empty',
    'cover_image' : 'is_image'
  })
  validator.validate()
  if validator.has_errors():
    errors = validator.get_errors()
    flash_data = {
      'status' : 'error',
      'message' : 'Form contains errors',
      'errors' : errors
    }
    response = FlashedRedirect('/admins/template_categories/new', request, flash_data, post_data)
  else:
    template_category = VideoTemplateCategory(**post_data)
    template_category.save()
    flash_data = {
      'status' : 'success',
      'message' : 'Template Category created successfully'
    }
    response = FlashedRedirect('/admins/template_categories', request, flash_data)
  return response

@admin_only
@flashable
def edit(request, id):
  response_dict = {}
  try:
    response_dict['flash_data'] = request.flash_data
    response_dict['form'] = request.form
  except:
    response_dict['form'] = VideoTemplateCategory.objects.get(pk=id)
  return render_to_response('admins/template_categories/edit.html', response_dict, RequestContext(request))

@admin_only
@post
def update(request, id):
  post_data = request.POST.dict()
  if 'cover_image' in post_data:
    del post_data['cover_image']
  validations = {
    'title' : 'is_not_empty',
    'description' : 'is_not_empty'
  }

  if 'cover_image' in request.FILES.dict().keys():
    post_data['cover_image'] = request.FILES['cover_image']
    validations['cover_image'] = 'is_image'
  validator = FormValidator(post_data, validations)
  validator.validate()
  if validator.has_errors():
    errors = validator.get_errors()
    flash_data = {
      'status' : 'error',
      'message' : 'Form contains errors',
      'errors' : errors
    }
    post_data['id']
    response = FlashedRedirect('/admins/template_categories/{}/edit'.format(id), request, flash_data, post_data)
  else:
    if 'cover_image' in post_data.keys():
      cover_image = post_data['cover_image']
      del post_data['cover_image']
    else:
      cover_image = None
    VideoTemplateCategory.objects.filter(pk=id).update(**post_data)
    template_category = VideoTemplateCategory.objects.get(pk=id)
    if cover_image is not None:
      try:
        import os
        os.remove(template_category.cover_image.path)
      except:
        pass
      template_category.cover_image = cover_image
      template_category.save()
    flash_data = {
      'status' : 'success',
      'message' : 'Template Category updated successfully'
    }
    response = FlashedRedirect('/admins/template_categories', request, flash_data)
  return response

  validator.validate()


@admin_only
def delete(request, id):
  try:
    #TO DO: while deleting a category, check if this is the only category some of the video templates have, if so then set their category as anonymous category object
    VideoTemplateCategory.objects.get(pk=id).delete()
    flash_data = {
      'status' : 'success',
      'message' : 'Template Category deleted successfully'
    }
  except:
    flash_data = {
      'status' : 'success',
      'message' : 'Template Category not found'
    }
  return FlashedRedirect('/admins/template_categories', request, flash_data)