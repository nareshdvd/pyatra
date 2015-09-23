from django.shortcuts import render
import subprocess
from subprocess import Popen
from aerenderpro.settings import *
import json
from django.views.decorators.csrf import csrf_exempt
import os
import shutil
from django.http import HttpResponse
from renderapi.tasks import render_process
def process(args):
  pr = Popen(args, stderr=subprocess.STDOUT)
  pr.wait()

@csrf_exempt
def render(request):
  if not request.POST:
    print "IAAMAER"
    return HttpResponse("OK")
  file = request.FILES.get('file')
  print file
  render_job_id = request.POST.get('render_job_id')
  print render_job_id
  zipped_file_path = os.path.join(MEDIA_ROOT, 'compressed_projects', file.name)
  print zipped_file_path
  unzipped_dir_path = os.path.join(MEDIA_ROOT, 'extracted_projects', render_job_id)
  print unzipped_dir_path
  if os.path.exists(unzipped_dir_path):
    shutil.rmtree(unzipped_dir_path)
  os.mkdir(unzipped_dir_path)
  open(os.path.join(MEDIA_ROOT, 'compressed_projects', file.name), 'wb+').write(file.read())
  process([
    'unzip',
    zipped_file_path,
    '-d',
    unzipped_dir_path
  ])
  print "IAMAAHERE"

  template_project_file_path = os.path.join(unzipped_dir_path, 'template.aep')
  output_dir = os.path.join(MEDIA_ROOT, 'final_videos', render_job_id)
  try:
    if not os.path.exists(output_dir):
      os.mkdir(output_dir)
    output_path = os.path.join(output_dir, 'video.mov')
  except Exception as ex:
    print ex
    return HttpResponse(json.dumps({'status' : 'hold', 'message' : 'On Hold for now'}), content_type='application/json')
  render_process.delay(render_job_id, [
    r'/Applications/Adobe After Effects CC 2014/aerender',
    '-project',
    template_project_file_path,
    '-comp',
    'final_comp',
    '-mp',
    '-output',
    output_path
  ])

  return HttpResponse(json.dumps({'status' : 'hold', 'message' : 'On Hold for now'}), content_type='application/json')

def restart_render(request):
  pass

def delete_job(request):
  pass

def send_finish_signal(request):
  pass
