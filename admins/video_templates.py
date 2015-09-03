from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from lib.decorators import *
from lib.validators import FormValidator
from yatra.models import Template, Category
from django.forms.models import model_to_dict
from lib.classes import JsonResponse

@admin_only
@flashable
def index(request):
  video_templates = Template.objects.filter(main_variation=True)
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
    'categories' : Category.objects.all()
  }
  try:
    response_dict['flash_data'] = request.flash_data
    response_dict['form'] = request.form
  except:
    response_dict['form'] = Template.create_new()
  return render_to_response('admins/video_templates/new.html', response_dict, RequestContext(request))

@admin_only
@post
def save(request):
  try:
    extra_variation_count = int(request.POST.get('extra_variation_count'))
  except:
    extra_variation_count = 0
  variation_id = request.POST.get('variation_id')
  categories = request.POST.getlist('categories[]')
  if type(categories).__name__ == 'list':
    categories = categories[0]
    categories = categories.split(',')
  post_data = request.POST.dict()
  template_all_variations = []
  if 'categories[]' in post_data:
    del post_data['categories[]']

  files_data = request.FILES.dict()
  variations = []
  demo_file = ''
  project_compressed_file = ''
  if 'demo_file' in files_data.keys():
    demo_file = files_data['demo_file']
  if 'project_compressed_file' in files_data.keys():
    project_compressed_file = files_data['project_compressed_file']
  main_variation = {
    'title' : post_data['title'],
    'categories' : categories,
    'demo_file' : demo_file,
    'project_compressed_file' : project_compressed_file,
    'main_variation' : 1,
    'variation_id' : variation_id,
    'variation_description' : post_data['variation_description']
  }
  template_all_variations.append(main_variation)
  validator = FormValidator(main_variation, {
    'title' : 'is_not_empty',
    'demo_file' : 'is_video',
    'categories' : 'is_array_not_empty',
    'project_compressed_file' : 'is_compressed',
    'variation_description' : 'is_not_empty'
  })
  errors = []
  if validator.has_errors():
    errs = validator.get_errors()
    if 'categories' in errs.keys():
      categories_error = errs['categories']
      del errs['categories']
      errs['categories[]'] = categories_error
    errors.append(validator.get_errors())
  for i in range(1,extra_variation_count+1):
    demo_file = ''
    project_compressed_file = ''
    if '{}_demo_file'.format(i) in files_data.keys():
      demo_file = files_data['{}_demo_file'.format(i)]
    if '{}_project_compressed_file'.format(i) in files_data.keys():
      project_compressed_file = files_data['{}_project_compressed_file'.format(i)]
    extra_variation = {
      'title' : post_data['{}_title'.format(i)],
      'categories' : categories,
      'demo_file' : demo_file,
      'project_compressed_file' : project_compressed_file,
      'main_variation' : 0,
      'variation_id' : variation_id,
      'variation_description' : post_data['{}_variation_description'.format(i)]
    }
    template_all_variations.append(extra_variation)
    validator = FormValidator(extra_variation, {
      'title' : 'is_not_empty',
      'demo_file' : 'is_video',
      'project_compressed_file' : 'is_compressed',
      'variation_description' : 'is_not_empty'
    })
    if validator.has_errors():
      variation_errors = validator.get_errors()
      new_variation_errors = {}
      for key, val in variation_errors.items():
        key = '{}_{}'.format(i, key)
        if 'categories' in key:
          new_variation_errors['{}[]'.format(key)] = val
        else:
          new_variation_errors[key] = val
      errors.append(new_variation_errors)
  response_dict = {}
  if(len(errors) == 0):
    for template_variation in template_all_variations:
      Template.add(template_variation)
    response_dict['status'] = 'success'
    response_dict['message'] = 'template(s) saved successfully'
  else:
    response_dict['status'] = 'error'
    response_dict['message'] = 'Form contains errors'
    response_dict['errors'] = errors
  return JsonResponse(response_dict)

def edit(request, id):
  response_dict = {
    'categories' : Category.objects.all()
  }
  try:
    response_dict['flash_data'] = request.flash_data
    response_dict['form'] = request.form
  except:
    object = Template.objects.get(pk=id)
    if object.main_variation == False:
      return HttpResponseRedirect('/admins/video_templates/{}/edit'.format(object.get_main_variation().id))
    else:
      only_variations = Template.objects.filter(variation_id=object.variation_id, main_variation = False)
    response_dict['extra_variations_count'] = len(only_variations)
    response_dict['form'] = [object]
    for variation in only_variations:
      response_dict['form'].append(variation)
    response_dict['template_categories'] = [str(obj.id) for obj in object.categories.all()]
  return render_to_response('admins/video_templates/edit.html', response_dict, RequestContext(request))

def update(request, id):
  try:
    extra_variation_count = int(request.POST.get('extra_variation_count'))
  except:
    extra_variation_count = 0
  variation_id = request.POST.get('variation_id')
  categories = request.POST.getlist('categories[]')
  if type(categories).__name__ == 'list':
    categories = categories[0]
    categories = categories.split(',')
  post_data = request.POST.dict()
  template_all_variations = []
  if 'categories[]' in post_data:
    del post_data['categories[]']

  files_data = request.FILES.dict()
  variations = []
  demo_file = ''
  project_compressed_file = ''
  if 'demo_file' in files_data.keys():
    demo_file = files_data['demo_file']
  if 'project_compressed_file' in files_data.keys():
    project_compressed_file = files_data['project_compressed_file']
  main_variation = {
    'id' : id,
    'title' : post_data['title'],
    'categories' : categories,
    'demo_file' : demo_file,
    'project_compressed_file' : project_compressed_file,
    'main_variation' : 1,
    'variation_id' : variation_id,
    'variation_description' : post_data['variation_description']
  }
  template_all_variations.append(main_variation)
  validator = FormValidator(main_variation, {
    'title' : 'is_not_empty',
    'demo_file' : 'is_video_or_empty',
    'categories' : 'is_array_not_empty',
    'project_compressed_file' : 'is_compressed_or_empty',
    'variation_description' : 'is_not_empty'
  })
  errors = []
  if validator.has_errors():
    errs = validator.get_errors()
    if 'categories' in errs.keys():
      categories_error = errs['categories']
      del errs['categories']
      errs['categories[]'] = categories_error
    errors.append(validator.get_errors())
  for i in range(1,extra_variation_count+1):
    demo_file = ''
    project_compressed_file = ''
    variation_obj_id = post_data['{}_id'.format(i)]
    if '{}_demo_file'.format(i) in files_data.keys():
      demo_file = files_data['{}_demo_file'.format(i)]
    if '{}_project_compressed_file'.format(i) in files_data.keys():
      project_compressed_file = files_data['{}_project_compressed_file'.format(i)]
    extra_variation = {
      'id' : variation_obj_id,
      'title' : post_data['{}_title'.format(i)],
      'categories' : categories,
      'demo_file' : demo_file,
      'project_compressed_file' : project_compressed_file,
      'main_variation' : 0,
      'variation_id' : variation_id,
      'variation_description' : post_data['{}_variation_description'.format(i)]
    }
    template_all_variations.append(extra_variation)
    if variation_obj_id == '' or variation_obj_id == None:
      validator = FormValidator(extra_variation, {
        'title' : 'is_not_empty',
        'demo_file' : 'is_video',
        'project_compressed_file' : 'is_compressed',
        'variation_description' : 'is_not_empty'
      })
    else:
      validator = FormValidator(extra_variation, {
        'title' : 'is_not_empty',
        'demo_file' : 'is_video_or_empty',
        'project_compressed_file' : 'is_compressed_or_empty',
        'variation_description' : 'is_not_empty'
      })
    if validator.has_errors():
      variation_errors = validator.get_errors()
      new_variation_errors = {}
      for key, val in variation_errors.items():
        key = '{}_{}'.format(i, key)
        if 'categories' in key:
          new_variation_errors['{}[]'.format(key)] = val
        else:
          new_variation_errors[key] = val
      errors.append(new_variation_errors)
  response_dict = {}
  if(len(errors) == 0):
    for template_variation in template_all_variations:
      if 'id' in template_variation.keys() and template_variation['id'] != '' and template_variation['id'] != None:
        Template.update(template_variation)
      else:
        Template.add(template_variation)
    response_dict['status'] = 'success'
    response_dict['message'] = 'template(s) saved successfully'
  else:
    response_dict['status'] = 'error'
    response_dict['message'] = 'Form contains errors'
    response_dict['errors'] = errors
  return JsonResponse(response_dict)

def delete(request, id):
  pass