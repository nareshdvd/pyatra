from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from yatra_app.models import Category, VideoTemplate, VideoSession, SessionItem, Steaker
from django.contrib.auth.models import User
import json
from IPython import embed
from django.db.models import Q
from lib.parser.parser import *
def home(request):
  categories = Category.objects.all()
  parent_templates = VideoTemplate.get_only_parent_templates()
  return render_to_response('yatra_app/home.html', {'categories' : categories, 'parent_templates' : parent_templates}, RequestContext(request))

def edit(request, id):
  image_edit_modal_needed = True
  video_edit_modal_needed = True
  if id != 0:
    category = Category.objects.get(id=id)
  else:
    category = '*'
  all_categories = Category.objects.all()
  template_id = int(request.GET.get('template_id'))
  steakers = Steaker.objects.all()
  return render_to_response('yatra_app/category.html', {'all_categories': all_categories, 'category' : category, 'template_id' : template_id, 'steakers' : steakers, 'image_edit_modal_needed' : image_edit_modal_needed, 'video_edit_modal_needed' : video_edit_modal_needed}, RequestContext(request))

def variations(request, category_id, template_id):
  parent_v_template = VideoTemplate.objects.get(id=template_id)
  variations_with_self = parent_v_template.variations_with_self()
  user = get_logged_in_user()
  #parent_template_variation_sessions = VideoSession.user_parent_template_variation_sessions(user.id, parent_v_template)
  #print parent_template_variation_sessions
  category = Category.objects.get(pk = category_id)
  return render_to_response('yatra_app/_variations.html', {'parent_v_template' : parent_v_template, 'category' : category, 'variations_with_self' : variations_with_self}, RequestContext(request))

def select_variation(request, category_id, template_id):
  user = get_logged_in_user()
  template = VideoTemplate.objects.get(pk = template_id)
  category = Category.objects.get(pk = category_id)
  video_session = user.video_sessions.filter(video_category_id=category_id, video_template_id=template_id).first()
  if video_session is None:
    video_session = VideoSession.new_session(user, template, category)
  response_json = render_to_response('yatra_app/_images_and_videos.json', {'video_session' : video_session, 'category' : category, 'template' : template})
  return HttpResponse(response_json, content_type = 'application/json')


def upload_images(request, category_id, template_id):
  user = get_logged_in_user()
  images = parse(request.POST.urlencode(), normalized=True)
  video_session = user.video_sessions.filter(video_category_id=category_id, video_template_id=template_id).first()
  category = Category.objects.get(pk = category_id)
  template = VideoTemplate.objects.get(pk = template_id)
  current_group = images['group']
  items_to_delete = []
  video_session.move_files_to_temp()
  for item in current_group:
    if item["item_file"] != "":
      if item["item_file"].startswith("/media/user_extracted_projects/"):
        file_name_number = item["item_file"].split("/")[-1].split(".")[0]
        if str(file_name_number) != str(item["item_number"]):
          # file is replaced
          session_item = video_session.session_items.filter(item_number=item["item_number"]).first()
          session_item.replace_from_temp(file_name_number)  
      else:
        session_item = video_session.session_items.filter(item_number=item["item_number"]).first()
        session_item.save_item_file(item["item_file"])
    else:
      items_to_delete.append(item["item_number"])
  if len(items_to_delete) != 0:
    other_items = video_session.session_items.filter(item_number__in=items_to_delete).filter(~Q( item_file = ''))
    for item in other_items:
      if item.item_type == "video":
        item.delete_webm_file()
      item.prevent_callback = True
      item.item_file = ''
      item.save()
  response_json = render_to_response('yatra_app/_images_and_videos.json', {'video_session' : video_session, 'category' : category, 'template' : template})
  return HttpResponse(response_json, content_type = 'application/json')

def render(request, category_id, template_id):
  user = get_logged_in_user()
  video_session = user.video_sessions.filter(video_category_id=category_id, video_template_id=template_id).first()
  video_session.render(category_id, template_id)
  return HttpResponse(json.dumps({"status" : "ok"}), content_type = 'application/json')

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def receive_video(request):
  mp4_file = request.FILES['mp4_file']
  video_session_id = request.POST.get('video_session_id')
  video_session = VideoSession.objects.get(pk = video_session_id)
  video_session.save_final_video(mp4_file)
  return HttpResponse(json.dumps({'status' : "OK"}), content_type = 'application/json')
  # return HttpResponse(json.dumps({"final_video" : video_session.final_video.url}), content_type = "application/json")

def look_for_video(request, category_id, template_id):
  user = get_logged_in_user()
  video_session = user.video_sessions.filter(video_category_id=category_id, video_template_id=template_id).first()
  retdata = {}
  if video_session.final_video:
    retdata['video_generated'] = True
    retdata['video_path'] = video_session.final_video.url
  else:
    retdata['video_generated'] = False
  return HttpResponse(json.dumps(retdata), content_type = "application/json")

def upload_videos(request, template_id):
  videos = request.FILES.getlist('dropzone_videos')
  return HttpResponse("OK");

def get_logged_in_user():
  return User.objects.get(pk=2)

# convert valuesqueryset to dict
def ValuesQuerySetToDict(vqs):
  return [item for item in vqs]