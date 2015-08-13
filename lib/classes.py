from django.http import HttpResponseRedirect, HttpResponse
from pyatra.settings import MEDIA_ROOT
import os
import json

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

  # media_file_path would be the relative path of the file you want to save after the /media directory in the project directory
  @classmethod
  def uploadfile(cls, file, media_file_path):
    # file.open()
    open(os.path.join(MEDIA_ROOT, media_file_path), 'wb+').write(file.read())
    # with open(os.path.join(MEDIA_ROOT, media_file_path), 'wb+') as destination:
    #     destination.write(file.read())

  @classmethod
  def get_video_session_file_path(cls, video_session, file_number, extension):
    vsdir = os.path.join(MEDIA_ROOT, 'uploads', video_session.session_id)
    if not os.path.exists(vsdir):
      os.mkdir(vsdir)

    return 'uploads/{}/{}.{}'.format(video_session.session_id, file_number, extension)