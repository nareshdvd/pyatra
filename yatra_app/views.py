from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from yatra_app.models import Category, VideoTemplate, VideoSession, SessionItem, Steaker
from django.contrib.auth.models import User
import json
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

def upload_images(request, template_id):
  images = request.FILES.getlist('dropzone_images')
  print request.FILES
  # user = get_logged_in_user()
  # video_template = VideoTemplate.objects.get(pk=template_id)
  # video_session = VideoSession.objects.filter(user=user, video_template=video_template).first()
  # if video_session is None:
  #   video_session = VideoSession.new_session(user, video_template)
  # for image in images:
  #   session_item = SessionItem.objects.filter(video_session=video_session).first()
  #   if session_item is not None:
  #     video_session.add_session_items()
  #   session_item = SessionItem.objects.filter(video_session=video_session).first()
  #   session_item.item_file = image
  #   session_item.save()

    
  return HttpResponse("OK");

def upload_videos(request, template_id):
  videos = request.FILES.getlist('dropzone_videos')
  return HttpResponse("OK");

def get_logged_in_user():
  return User.objects.get(pk=2)