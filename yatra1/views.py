from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect,HttpResponse
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
  template_categories = Category.objects.all()
  response_dict = {
    'flash_data' : flash_data,
    'template_categories' : template_categories
  }

  return render_to_response('yatra/categories.html', response_dict, RequestContext(request))

@token_user_only
def select_category(request, id):
  try:
    category = Category.objects.get(pk=id)
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

  category_id = request.session['selected_category_id']
  category = Category.objects.get(pk=category_id)
  category_templates = category.category_templates.all()
  if category_templates.count() == 0:
    flash_data = {
      'status' : 'error',
      'message' : 'Templates are not added to this category yet'
    }
    response = FlashedRedirect('/yatra/categories', request, flash_data)
  else:
    response_dict = {
      'category_templates' : category_templates,
      'category' : category
    }
    try:
      flash_data = request.flash_data
      response_dict['flash_data'] = flash_data
    except:
      pass
    response = render_to_response('yatra/templates.html', response_dict, RequestContext(request))
  # except:
  #   flash_data = {
  #     'status' : 'error',
  #     'message' : 'Category not found'
  #   }
  #   response = FlashedRedirect('/yatra/categories', request, flash_data)
  return response


@token_user_only
def select_template(request, category_id, id):
  try:
    template = Template.objects.get(pk=id)
    video_session = VideoSession.get_or_generate(request.user, template)
    request.session['video_session_id'] = video_session.id
    request.session['category_id'] = category_id
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
    category_id = request.session['category_id']
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
  category = Category.objects.get(pk=category_id)
  response_dict = {
    'video_session' : video_session,
    'category' : category,
    'video_template' : video_template,
    'items' : items
  }
  response = render_to_response('yatra/items.html', response_dict, RequestContext(request))
  return response


def show_upload(request, item_number):
  item_number = int(item_number)
  if request.is_ajax():
    get_data = request.GET.dict()
    response_dict = {}
    response_dict['item_number'] = item_number
    video_session_id = request.session['video_session_id']
    video_session = VideoSession.objects.get(pk=video_session_id)
    video_template = video_session.video_template
    response_dict['video_template'] = video_template
    item = video_session.contents.filter(content_order=item_number).first()
    items_info = video_template.get_items_info()
    item_info = items_info[item_number - 1]
    response_dict['item_info'] = item_info
    if item is not None:
      response_dict['item'] = item
    else:
      response_dict['item'] = None
    return render_to_response("yatra/upload_form.html", response_dict, RequestContext(request))
  else:
    return HttpResponse("Normal requests not allowed")

@post
def save_item(request):
  files_data = request.FILES.dict()
  post_data  = request.POST.dict()
  file_number = post_data['file_number']
  file_type = post_data['file_type']
  file = files_data['fi_{}'.format(file_number)]
  video_session_id = request.session['video_session_id']
  video_session = VideoSession.objects.get(pk=video_session_id)
  response_dict = {}
  if file_type == 'image':
    item = video_session.add_photo({
      'attachment' : file,
      'content_order' : file_number
    })
    response_dict = {
      'status' : 'success',
      'attachment_url' : item.attachment.url,
      'resized_url' : item.resized('600X337')
    }
  else:
    item = video_session.add_video({
      'attachment' : file,
      'content_order' : file_number
    })
    response_dict = {
      'status' : 'success'
    }
  return JsonResponse(response_dict)


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

def get_item_crop(request, item_number):
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
    return render_to_response('yatra/crop_item.html', response_dict, RequestContext(request))
  else:
    return render_to_response('yatra/crop_item.html', response_dict, RequestContext(request))

from PIL import Image, ImageOps
def post_item_crop(request, item_number):
  video_session_id = request.session['video_session_id']
  video_session = VideoSession.objects.get(pk=video_session_id)
  video_template = video_session.video_template
  item = video_session.viewablecontents.filter(content_order=item_number).first()
  items_info = video_template.get_items_info()
  item_info = items_info[int(item_number) - 1]

  post_data = request.POST.dict()
  crop_x = float(post_data['x'])
  crop_y = float(post_data['y'])
  crop_width = float(post_data['width'])
  crop_height = float(post_data['height'])
  ui_width = 600
  ui_height = 337

  orig_width = 1920
  orig_height = 1080

  scale_width = ((orig_width)/(ui_width*1.0))
  scale_height = ((orig_height)/(ui_height*1.0))
  print scale_width
  print scale_height
  import math
  left = int(math.ceil(crop_x * scale_width))
  top = int(math.ceil(crop_y * scale_height))
  right = int(math.ceil(left + (crop_width  * scale_width)))
  bottom = int(math.ceil(top + (crop_height * scale_height)))

  path = item.attachment.path
  new_path = item.attachment.path.replace(".jpeg", "_cropped.jpeg")
  print new_path
  image = Image.open(path)
  if image.mode not in ("L", "RGB"):
    image = image.convert("RGB")
  image = image.crop((left, top, right, bottom))
  image = image.rotate(180+90)
  image.save(new_path, "jpeg", quality=100)
  return JsonResponse({'status' : 'success', 'message' : 'cropped successfully'})


def save_modified_image(request, item_number):
  attachment = request.POST.get('attachment')
  video_session_id = request.session['video_session_id']
  video_session = VideoSession.objects.get(pk=video_session_id)
  video_template = video_session.video_template
  video_session.add_base64_photo(item_number, attachment)
  return JsonResponse({'status' : 'success', 'message' : 'saved successfully'})


def test(request):
  data = request.POST.get('tttt')
  print data
  print request.method
  return render_to_response('yatra/test.html', {}, RequestContext(request))




