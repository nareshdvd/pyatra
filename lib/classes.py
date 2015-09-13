from django.http import HttpResponseRedirect, HttpResponse
from pyatra.settings import MEDIA_ROOT
import os
import json
import base64
from lib.helpers import run_process

class FlashedRedirect(HttpResponseRedirect):
  def __init__(self, redirect_to, request, flash_data, form=None, *args, **kwargs):
    request.session['flash_data'] = flash_data
    if form is not None:
      request.session['form'] = form
    super(FlashedRedirect, self).__init__(redirect_to, *args, **kwargs)

class JsonResponse(HttpResponse):
  def __init__(self, response_dict):
    json_data = json.dumps(response_dict)
    super(JsonResponse, self).__init__(json_data, content_type="application/json")


class FileHandler(object):
  @classmethod
  def get_extension(cls, file):
    return file.content_type.split('/')[1]

  @classmethod
  def get_extension_of_base64(cls, base64str):
    if base64str.startswith('data:image/png;base64,'):
      return 'png'
    elif base64str.startswith('data:image/jpeg;base64,'):
      return 'jpeg'
    else:
      return None

  @classmethod
  def remove_extra_info_from_base64(cls, base64str):
    if base64str.startswith('data:image/png;base64,'):
      return base64str.replace('data:image/png;base64,','')
    elif base64str.startswith('data:image/jpeg;base64,'):
      return base64str.replace('data:image/jpeg;base64,','')

  # media_file_path would be the relative path of the file you want to save after the /media directory in the project directory
  @classmethod
  def uploadfile(cls, file, media_file_path):
    open(os.path.join(MEDIA_ROOT, media_file_path), 'wb+').write(file.read())


  @classmethod
  def uploadbase64file(cls, base64str, media_file_path):
    base64str = base64str.replace(" ", "+")
    base64str_decoded = base64.b64decode(base64str)
    image_path = os.path.join(MEDIA_ROOT, media_file_path)
    fh = open(image_path, 'wb')
    fh.write(base64str_decoded)
    fh.close()


    #open(os.path.join(MEDIA_ROOT, media_file_path), 'wb+').write(file.read())

  @classmethod
  def get_video_session_file_path(cls, video_session, file_number, extension):
    vsdir = os.path.join(MEDIA_ROOT, 'uploads', video_session.session_id)
    if not os.path.exists(vsdir):
      os.mkdir(vsdir)

    return 'uploads/{}/{}.{}'.format(video_session.session_id, file_number, extension)

  @classmethod
  def convert_video(cls, original_path, input_format, output_format):
    newpath = original_path.replace(input_format, output_format)
    run_process([
      'ffmpeg',
      '-i',
      original_path,
      newpath
    ])