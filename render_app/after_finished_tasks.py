import requests
from pyatra.settings import MEDIA_ROOT, MAIN_SERVER
import os
def send_notification_about_video_generated(video_session_id, output_file_mp4_path):
  files = {'output_file': open(output_file_mp4_path, 'rb')}
  r = requests.post("{}/{}/{}".format(MAIN_SERVER, 'render_finished', video_session_id), files = files, data = {'video_session_id' : video_session_id})
  pass

def delete_file(file_path):
  if os.path.exists(file_path):
    os.remove(file_path)