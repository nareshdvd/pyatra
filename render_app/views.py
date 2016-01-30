from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from IPython import embed
from pyatra.settings import MEDIA_ROOT, MAIN_SERVER
import os
import shutil
import requests
import subprocess
from subprocess import Popen
from render_app.lib import process
from render_app.tasks import delayed_process
import requests
import json
# Create your views here.

@csrf_exempt
def render(request, category_id, template_id):
  print "I m here"
  video_session_id = request.POST.get('video_session_id')
  zipped_project = request.FILES['zipped_project']
  save_zipped_project(video_session_id, zipped_project)
  extract_zipped_project(video_session_id, zipped_project)
  process_set_for_rendering = render_project(video_session_id, zipped_project)
  return HttpResponse(json.dumps({'status' : process_set_for_rendering}), content_type='application/json')


def get_video_session_dir(video_session_id):
  return os.path.join(MEDIA_ROOT, str(video_session_id))

def save_zipped_project(video_session_id, zipped_project_file):
  video_session_dir = get_video_session_dir(video_session_id)
  zipped_project_path = os.path.join(video_session_dir, str(zipped_project_file))
  if not os.path.exists(video_session_dir):
    os.mkdir(video_session_dir)
  if os.path.exists(zipped_project_path):
    os.remove(zipped_project_path)

  with open(zipped_project_path, 'wb+') as destination:
    for chunk in zipped_project_file.chunks():
      destination.write(chunk)

def extract_zipped_project(video_session_id, zipped_project_file):
  video_session_dir = get_video_session_dir(video_session_id)
  zipped_project_path = os.path.join(video_session_dir, str(zipped_project_file))
  project_name = zipped_project_path.split("/")[-1].replace(".zip", "")
  if os.path.exists(zipped_project_path.replace(".zip", "")):
    shutil.rmtree(zipped_project_path.replace(".zip", ""))
  project_path = os.path.join(video_session_dir, project_name)
  if os.path.exists(project_path):
    shutil.rmtree(project_path)
  os.mkdir(project_path)
  process([
    'unzip',
    zipped_project_path,
    '-d',
    project_path
  ])


def render_project(video_session_id, zipped_project_file):
  video_session_dir = get_video_session_dir(video_session_id)
  zipped_project_path = os.path.join(video_session_dir, str(zipped_project_file))
  project_name = zipped_project_path.split("/")[-1].replace(".zip", "")
  project_path = os.path.join(video_session_dir, project_name)
  template_file_path = os.path.join(project_path, 'template.aep')
  output_file_path = os.path.join(video_session_dir, 'final_video.mp4')
  rendered = render_process(template_file_path, output_file_path)
  return True


def render_process(template_file_path, output_file_path):
  process_params = [
    r'/Applications/Adobe After Effects CC 2014/aerender',
    '-project',
    template_file_path,
    '-comp',
    'final_comp',
    '-mp',
    '-output',
    output_file_path
  ]
  print "I M IN DELAYED PROCESS START PROCESS"
  delayed_process.delay(process_params)
  return True
