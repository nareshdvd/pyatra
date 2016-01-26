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
# Create your views here.

@csrf_exempt
def render(request):
  category_id = request.POST.get('category_id')
  template_id = request.POST.get('template_id')
  video_session_id = request.POST.get('video_session_id')
  zipped_project = request.FILES['zipped_project']
  save_zipped_project(video_session_id, zipped_project)
  extract_zipped_project(video_session_id, zipped_project)
  mp4_file = render_project(video_session_id, zipped_project)
  import requests
  files = {'mp4_file': open(mp4_file, 'rb')}
  r = requests.post("{}/{}".format(MAIN_SERVER, 'receive_video'), files = files, data = {'category_id' : category_id, 'template_id' : template_id, 'video_session_id' : video_session_id})
  return HttpResponse("OK")


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
  # process([aerender params here])
  return os.path.join(MEDIA_ROOT, '3.mp4')


def process(args):
  pr = Popen(args, stderr=subprocess.STDOUT)
  pr.wait()
