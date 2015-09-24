# session variables: selected_category_id, selected_template_id, current_video_session_id
from django.shortcuts import render, render_to_response
from lib.classes import *
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from yatra.models import *

# Create your views here.

def home(request):
  return render_to_response('yatra/home.html', {}, RequestContext(request))

def view_categories(request):
  response_dict = {
    'categories' : Category.objects.all()
  }
  return render_to_response('yatra/view_categories.html', response_dict, RequestContext(request))

def select_category(request, id):
  try:
    category = Category.objects.get(pk=id)
  except:
    return HttpResponseRedirect('/yatra/categories')
  request.session['selected_category_id'] = category.id
  return HttpResponseRedirect('/yatra/templates')

def view_templates(request):
  if 'selected_category_id' in request.session.keys():
    selected_category_id = request.session['selected_category_id']
  else:
    return HttpResponseRedirect('/yatra/categories')

  selected_category = Category.objects.get(pk=selected_category_id)
  templates = selected_category.main_template_variations.all()
  response_dict = {
    'selected_category' : selected_category,
    'templates' : templates
  }
  return render_to_response('yatra/view_templates.html', response_dict, RequestContext(request))

def select_template(request, id):
  try:
    template = Template.objects.get(pk=id)
  except:
    return HttpResponseRedirect('/yatra/templates')
  request.session['selected_template_id'] = template.id
  video_session = VideoSession.get_or_generate(request.user, template)
  request.session['current_video_session_id'] = video_session.id
  return HttpResponseRedirect('/yatra/items')

def view_variations(request, variation_id):
  selected_category_id = request.session['selected_category_id']
  selected_category = Category.objects.get(pk=selected_category_id)
  templates = Template.objects.filter(variation_id=variation_id)
  response_dict = {
    'selected_category' : selected_category,
    'templates' : templates
  }
  return render_to_response('yatra/view_variations.html', response_dict, RequestContext(request))


def view_items(request):
  if 'current_video_session_id' in request.session.keys():
    current_video_session_id = request.session['current_video_session_id']
    current_video_session = VideoSession.objects.get(id=current_video_session_id)
  else:
    return HttpResponseRedirect('/yatra/templates')
  selected_category_id = request.session['selected_category_id']
  selected_category = Category.objects.get(pk=selected_category_id)
  select_template_id = request.session['selected_template_id']
  selected_template = Template.objects.get(pk=select_template_id)

  mock_items = selected_template.get_items_info()
  uploaded_items =current_video_session.viewablecontents.all()

  response_dict = {
    'current_video_session' : current_video_session,
    'selected_category' : selected_category,
    'selected_template' : selected_template,
    'mock_items' : mock_items,
    'uploaded_items' : uploaded_items
  }
  return render_to_response('yatra/view_items.html', response_dict, RequestContext(request))

def view_edit_item(request, item_number):
  item_number = int(item_number)
  response_dict = {}
  response_dict['item_number'] = item_number
  video_session_id = request.session['current_video_session_id']
  session = VideoSession.objects.get(pk=video_session_id)
  template = session.video_template
  response_dict['template'] = template
  item = session.contents.filter(content_order=item_number).first()
  items_info = template.get_items_info()
  item_info = items_info[item_number - 1]
  response_dict['item_info'] = item_info
  if item is not None:
    response_dict['item'] = item
  else:
    response_dict['item'] = None
  if item_info['file_type'] == 'image':
    return render_to_response("yatra/image_edit_modal.html", response_dict, RequestContext(request))
  else:
    selected_category_id = request.session['selected_category_id']
    selected_category = Category.objects.get(pk=selected_category_id)
    response_dict['selected_category'] = selected_category
    return render_to_response("yatra/video_edit_modal.html", response_dict, RequestContext(request))

def upload_item(request, item_number):
  files_data = request.FILES.dict()
  post_data  = request.POST.dict()
  file_number = item_number
  file_type = post_data['file_type']
  file = files_data['file']
  video_session_id = request.session['current_video_session_id']
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
      'status' : 'success',
      'attachment_url' : item.attachment.url,
    }
  return JsonResponse(response_dict)

def upload_base64_image_item(request, item_number):
  attachment = request.POST.get('attachment')
  video_session_id = request.session['current_video_session_id']
  video_session = VideoSession.objects.get(pk=video_session_id)
  video_template = video_session.video_template
  item = video_session.add_base64_photo(item_number, attachment)
  response_dict = {
    'status' : 'success',
    'attachment_url' : item.attachment.url,
    'resized_url' : item.resized('600X337')
  }

  return JsonResponse(response_dict)

from PIL import Image, ImageOps
def save_cropped_image(request, item_number):
  video_session_id = request.session['current_video_session_id']
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

def save_cropped_video(request, item_number):
  vid_start = request.POST.get('vid_start')
  vid_end = request.POST.get('vid_end')
  video_session_id = request.session['current_video_session_id']
  video_session = VideoSession.objects.get(pk=video_session_id)
  video_template = video_session.video_template
  item = video_session.viewablecontents.filter(content_order=item_number).first()
  item.crop({'vid_start' : vid_start, 'vid_end' : vid_end})
  return JsonResponse({'status' : 'success', 'message' : 'cropped successfully'})


def render(request):
  video_session_id = request.session['current_video_session_id']
  video_session = VideoSession.objects.get(pk=video_session_id)
  video_template = video_session.video_template
  data = video_template.render(video_session)
  return JsonResponse(data)


def receive_rendered_video(request):
  video_file = request.FILES.get('file')
  render_job_id = request.POST.get('render_job_id')
  render_job = RenderJob.objects.get(pk=render_job_id)
  render_job.finish('Video generated', video_file)
  return JsonResponse({'status' : 'success'})


def final_video(request):
  video_session_id = request.session['current_video_session_id']
  video_session = VideoSession.objects.get(pk=video_session_id)
  if video_session.video_generated == False:
    return HttpResponseRedirect('/yatra/items')
  response_dict = {
    'video_session' : video_session
  }
  selected_category_id = request.session['selected_category_id']
  selected_category = Category.objects.get(pk=selected_category_id)
  response_dict['selected_category'] = selected_category
  return render_to_response("yatra/final_video.html", response_dict, RequestContext(request))