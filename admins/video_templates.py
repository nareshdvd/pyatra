from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from lib.decorators import *
from lib.validators import FormValidator
from yatra.models import VideoTemplate, VideoTemplateCategory
from django.forms.models import model_to_dict

@admin_only
@flashable
def index(request):
  video_templates = VideoTemplate.objects.all()
  response_dict = {
    'video_templates' : video_templates
  }
  try:
    response_dict['flash_data'] = request.flash_data
  except:
    pass
  return render_to_response('admins/video_templates/index.html', response_dict, RequestContext(request))

@admin_only
@flashable
def new(request):
  response_dict = {
    'categories' : VideoTemplateCategory.objects.all()
  }
  try:
    response_dict['flash_data'] = request.flash_data
    response_dict['form'] = request.form
  except:
    pass
  return render_to_response('admins/video_templates/new.html', response_dict, RequestContext(request))

@admin_only
@post
def save(request):
  categories = request.POST.getlist('categories[]')
  post_data = request.POST.dict()
  if 'categories[]' in post_data:
    del post_data['categories[]']
  post_data['categories'] = categories
  files_data = request.FILES.dict()
  demo_file = ''
  project_compressed_file = ''
  if 'demo_file' in files_data.keys():
    demo_file = files_data['demo_file']
  if 'project_compressed_file' in files_data.keys():
    project_compressed_file = files_data['project_compressed_file']


  post_data['demo_file'] = demo_file
  post_data['project_compressed_file'] = project_compressed_file
  validator = FormValidator(post_data, {
    'title' : 'is_not_empty',
    'demo_file' : 'is_video',
    'categories' : 'is_array_not_empty',
    'project_compressed_file' : 'is_compressed'
  })
  if validator.has_errors():
    flash_data = {
      'status' : 'error',
      'message' : 'Form contains errors',
      'errors'  : validator.get_errors()
    }
    redirect_url = reverse('admins:new_video_template')
  else:
    video_template = VideoTemplate.add({
      'title' : post_data['title'],
      'demo_file' : demo_file,
      'categories' : post_data['categories'],
      'project_compressed_file' : project_compressed_file
    })
    flash_data = {
      'status' : 'success',
      'message' : 'Video Template Saved successfully'
    }
    redirect_url = reverse('admins:video_templates')
  response_dict = {
    'flash_data' : flash_data
  }
  del post_data['demo_file']
  del post_data['project_compressed_file']
  return FlashedRedirect(redirect_url, request, flash_data, post_data)

def edit(request, id):
  response_dict = {
    'categories' : VideoTemplateCategory.objects.all()
  }
  try:
    response_dict['flash_data'] = request.flash_data
    response_dict['form'] = request.form
  except:
    object = VideoTemplate.objects.get(pk=id)
    response_dict['form'] = model_to_dict(object)
    response_dict['form']['categories'] = [str(obj.id) for obj in object.categories.all()]
  return render_to_response('admins/video_templates/edit.html', response_dict, RequestContext(request))

def update(request, id):
  categories = request.POST.getlist('categories[]')
  post_data = request.POST.dict()
  post_data['id'] = id
  if 'demo_file' in post_data.keys():
    del post_data['demo_file']

  if 'project_compressed_file' in post_data.keys():
    del post_data['project_compressed_file']

  if 'categories[]' in post_data:
    del post_data['categories[]']

  post_data['categories'] = categories
  files_data = request.FILES.dict()
  demo_file = ''
  project_compressed_file = ''
  validations = {
    'title' : 'is_not_empty',
    'categories' : 'is_array_not_empty'
  }
  if 'demo_file' in files_data.keys():
    demo_file = files_data['demo_file']
    validations['demo_file'] = 'is_video'
    post_data['demo_file'] = demo_file

  if 'project_compressed_file' in files_data.keys():
    project_compressed_file = files_data['project_compressed_file']
    validations['project_compressed_file'] = 'is_compressed'
    post_data['project_compressed_file'] = project_compressed_file

  validator = FormValidator(post_data, validations)
  if validator.has_errors():
    flash_data = {
      'status' : 'error',
      'message' : 'Form contains errors',
      'errors'  : validator.get_errors()
    }
    redirect_url = '/admins/video_templates/{}/edit'.format(id)
  else:
    # update_data = {
    #   'title' : post_data['title'],
    #   'demo_file' : demo_file,
    #   'categories' : post_data['categories'],
    #   'project_compressed_file' : project_compressed_file
    # }
    video_template = VideoTemplate.update(post_data)
    flash_data = {
      'status' : 'success',
      'message' : 'Video Template Saved successfully'
    }
    redirect_url = reverse('admins:video_templates')
  response_dict = {
    'flash_data' : flash_data
  }
  if 'demo_file' in post_data.keys():
    del post_data['demo_file']
  if 'project_compressed_file' in post_data.keys():
    del post_data['project_compressed_file']
  return FlashedRedirect(redirect_url, request, flash_data, post_data)

def delete(request, id):
  pass