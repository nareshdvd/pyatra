from aerenderpro import celery_app
import subprocess
from subprocess import Popen
import os
import requests
from aerenderpro.settings import *
from renderapi.realtime_info import *
def sys_process(args):
  pr = Popen(args, stderr=subprocess.STDOUT)
  pr.wait()


@celery_app.task
def test_render_process(render_job_id, process_params):
  import time
  time.sleep(10)
  send_realtime_info({'render_process_status': 'finished'})



@celery_app.task
def render_process(render_job_id, process_params):
  sys_process(process_params)
  #convert video to mp4
  mov_path = os.path.join(MEDIA_ROOT, 'final_videos', render_job_id, 'video.mov')
  final_video_path = os.path.join(MEDIA_ROOT, 'final_videos', render_job_id, 'video.mp4')
  sys_process([
    'ffmpeg',
    '-i',
    mov_path,
    '-qscale',
    '0',
    final_video_path
  ])
  finish_url = 'http://dev.photoyatra.in/yatra/receive_rendered_video'
  files = {'file' : open(final_video_path, 'rb')}
  data = requests.post(finish_url, data={'render_job_id' : render_job_id}, files=files).json()
  delete_mov.delay(mov_path)

@celery_app.task
def delete_mov(path):
  if os.path.exists(path):
    os.remove(path)
