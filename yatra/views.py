from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from lib.decorators import *
from lib.validators import FormValidator
from lib.classes import *

from yatra.models import *



def home(request):
  return HttpResponseRedirect('/accounts/signin')

@token_user_only
@flashable
def categories(request):
  try:
    flash_data = request.flash_data
  except:
    flash_data = {}
  template_categories = VideoTemplateCategory.objects.all()
  response_dict = {
    'flash_data' : flash_data,
    'template_categories' : template_categories
  }

  return render_to_response('yatra/categories.html', response_dict, RequestContext(request))

@token_user_only
def select_category(request, id):
  try:
    category = VideoTemplateCategory.objects.get(pk=id)
    request.session['selected_category_id'] = id
    flash_data = {}
    redirect_url = '/yatra/templates'
  except Exception as e:
    flash_data = {
      'status' : 'error',
      'message' : 'Category not found'
    }
    redirect_url = '/yatra/categories'
  return FlashedRedirect(redirect_url, request, flash_data)


@token_user_only
@flashable
def templates(request):
  try:
    category_id = request.session['selected_category_id']
    category = VideoTemplateCategory.objects.get(pk=category_id)
    category_templates = category.category_templates.all()
    if category_templates.count() == 0:
      flash_data = {
        'status' : 'error',
        'message' : 'Templates are not added to this category yet'
      }
      response = FlashedRedirect('/yatra/categories', request, flash_data)
    else:
      response_dict = {
        'category_templates' : category_templates
      }
      try:
        flash_data = request.flash_data
        response_dict['flash_data'] = flash_data
      except:
        pass
      response = render_to_response('yatra/templates.html', response_dict, RequestContext(request))
  except:
    flash_data = {
      'status' : 'error',
      'message' : 'Category not found'
    }
    response = FlashedRedirect('/yatra/categories', request, flash_data)
  return response


@token_user_only
def select_template(request, id):
  try:
    template = VideoTemplate.objects.get(pk=id)
    video_session = VideoSession.generate(request.user, template)
    request.session['video_session_id'] = video_session.id
    redirect_url = '/yatra/items'
    flash_data = {}
  except:
    flash_data = {
      'status' : 'error',
      'message' : 'Template not found'
    }
    redirect_url = '/yatra/templates'
  return FlashedRedirect(redirect_url, request, flash_data)

@token_user_only
def items(request):
  try:
    video_session_id = request.session['video_session_id']
  except:
    flash_data = {
      'status' : 'error',
      'message' : 'Please select a template'
    }
    redirect_url = '/yatra/templates'
    return FlashedRedirect(redirect_url, request, flash_data)
  video_session = VideoSession.objects.get(pk=video_session_id)
  items = YatraContent.objects.filter(video_session=video_session)
  video_template = video_session.video_template
  response_dict = {
    'video_session' : video_session,
    'video_template' : video_template,
    'items' : items
  }
  response = render_to_response('yatra/items.html', response_dict, RequestContext(request))
  return response

@post
def save_item(request):
  files_data = request.FILES.dict()
  post_data  = request.POST.dict()
  file_number = post_data['file_number']
  file_type = post_data['file_type']
  file = files_data['fi_{}'.format(file_number)]
  video_session_id = request.session['video_session_id']
  video_session = VideoSession.objects.get(pk=video_session_id)
  if file_type == 'image':
    video_session.add_photo({
      'attachment' : file,
      'content_order' : file_number
    })
  else:
    video_session.add_video({
      'attachment' : file,
      'content_order' : file_number
    })
  return HttpResponseRedirect('/yatra/items/{}'.format(file_number))

def get_item(request, item_number):
  video_session_id = request.session['video_session_id']
  video_session = VideoSession.objects.get(pk=video_session_id)
  video_template = video_session.video_template
  item = video_session.viewablecontents.filter(content_order=item_number).first()
  items_info = video_template.get_items_info()
  item_info = items_info[int(item_number) - 1]
  response_dict = {
    'item' : item,
    'item_info' : item_info
  }
  if request.is_ajax():
    return render_to_response('yatra/ajax_item.html', response_dict, RequestContext(request))
  else:
    return render_to_response('yatra/item.html', response_dict, RequestContext(request))


