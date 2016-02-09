from __future__ import unicode_literals

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
import subprocess
from subprocess import Popen
from django.db.models.signals import post_save, pre_delete
from pyatra.settings import MEDIA_ROOT, RENDERER_SERVER
import os
from os import listdir
import shutil
from os.path import isfile, join
from yatra_app.imagegenerators import MainImageVariation
# Create your models here.

def process(args):
  pr = Popen(args, stderr=subprocess.STDOUT)
  pr.wait()

class Category(models.Model):
  title = models.CharField(max_length = 500, null = False, blank = False)
  cover_image = models.ImageField(upload_to='category_covers')
  created_at = models.DateTimeField(auto_now_add = True)
  updated_at = models.DateTimeField(auto_now = True)
  def __str__(self):
    return self.title

  def parent_templates(self):
    return self.video_templates.filter(parent_id=None)



class VideoTemplate(MPTTModel):
  title = models.CharField(max_length = 1000, null = False, blank = False)
  description = models.TextField(null = False, blank = False)
  cover_image = models.ImageField(upload_to='video_template_covers')
  categories = models.ManyToManyField(Category, related_name='video_templates')
  parent = TreeForeignKey('self', null=True, blank=True, related_name='variations', db_index=True)
  compressed_file = models.FileField(upload_to='compressed_projects', null = False, blank = False)
  demo_file = models.FileField(upload_to='demo_files', null = False, blank = False)
  created_at = models.DateTimeField(auto_now_add = True)
  updated_at = models.DateTimeField(auto_now = True)
  class MPTTMeta:
    order_insertion_by = ['title']

  def __str__(self):
    return self.title

  @classmethod
  def get_only_parent_templates(cls):
    return cls.objects.filter(parent=None)

  def variations_with_self(self):
    return self.variations.all() | VideoTemplate.objects.filter(pk=self.id)
    # return list(chain([self], variations))

  def images_count(self):
    import random
    return random.randint(4, 5)

  def videos_count(self):
    import random
    return random.randint(4, 5)

  def extract_project(self, extract_dir, delete_earlier = False):
    project_dir_name = self.project_dir_name()
    do_extract = False
    if os.path.exists(os.path.join(extract_dir, project_dir_name)):
      if delete_earlier:
        shutil.rmtree(os.path.join(extract_dir, project_dir_name))
        do_extract = True
      else:
        do_extract = False
    else:
      do_extract = True

    if do_extract:
      if self.compressed_file.path.endswith('.zip'):
        process([
          'unzip',
          self.compressed_file.path,
          '-d',
          extract_dir
        ])
        extension = '.zip'
      elif self.compressed_file.path.endswith('.tar.gz'):
        process([
          'tar',
          '-zxvf',
          self.compressed_file.path,
          '-C',
          extract_dir
        ])
        extension = '.tar'
  def project_dir_name(self):
    return self.compressed_file.path.split('/')[-1].split(".")[0]

def post_save_for_video_templates(sender, instance, **kwargs):
  extract_dir = os.path.join(MEDIA_ROOT, 'extracted_projects')
  instance.extract_project(extract_dir, True)

post_save.connect(post_save_for_video_templates, sender=VideoTemplate)

def final_video_relative_upload_path(instance, filename):
  return os.path.join(instance.extract_dir(True), filename)

class VideoSession(models.Model):
  session_id = models.CharField(max_length = 255, null = False, blank = False)
  user = models.ForeignKey(User, related_name = 'video_sessions')
  video_template = models.ForeignKey(VideoTemplate, related_name = 'template_video_sessions')
  video_category = models.ForeignKey(Category, related_name = 'category_video_sessions')
  final_video = models.FileField(upload_to=final_video_relative_upload_path, null = True, blank = True, default = '')
  rendering_started = models.BooleanField(default=False)
  rendering_finished = models.BooleanField(default=False)
  rendering_percentage = models.IntegerField(default=0)

  def save_final_video(self, mp4_file):
    if self.final_video and os.path.exists(self.final_video.path):
      os.remove(self.final_video.path)
    self.final_video = mp4_file
    self.prevent_callback = True
    self.save()

  @classmethod
  def new_session(cls, user, video_template, video_category):
    import uuid
    video_session = VideoSession.objects.filter(user=user, video_template=video_template).first()
    if video_session is None:
      video_session = VideoSession(**{
          'session_id' : str(uuid.uuid4()),
          'user_id' : user.id,
          'video_template_id' : video_template.id,
          'video_category_id' : video_category.id
        }
      )
      video_session.save()
    return video_session

  def extract_dir(self, relative=False):
    if relative:
      return 'user_extracted_projects/{}'.format(self.session_id)
    else:
      return os.path.join(MEDIA_ROOT, 'user_extracted_projects', self.session_id)

  def project_dir(self, relative = False):
    return os.path.join(self.extract_dir(relative), self.video_template.project_dir_name())

  def footage_item_dir(self, relative = False):
    return os.path.join(self.project_dir(relative), 'footage_items')

  def extract_project(self):
    print self.extract_dir(False)
    if not os.path.exists(self.extract_dir(False)):
      os.mkdir(self.extract_dir(False))
    self.video_template.extract_project(self.extract_dir(False), False)

  def move_files_to_temp(self):
    temp_dir_name = os.path.join(self.extract_dir(False), "temp")
    if os.path.exists(temp_dir_name):
      print "deleting temp directory"
      shutil.rmtree(temp_dir_name)
    os.mkdir(temp_dir_name)
    for session_item in self.session_items.all():
      if session_item.item_file and os.path.exists(session_item.item_file.path):
        shutil.copy(session_item.item_file.path, temp_dir_name)
        if session_item.item_type != "image":
          shutil.copy(session_item.webm_path(), temp_dir_name)


  def add_session_items(self):
    self.extract_project()
    footage_items_dir = self.footage_item_dir(False)
    onlyfiles = [ f for f in listdir(footage_items_dir) if (isfile(join(footage_items_dir,f)) and unicode(f.split('/')[-1].split('.')[0]).isnumeric()) ]
    def numeric_compare(i, j):
      i = int(i.split('.')[0])
      j = int(j.split('.')[0])
      return i - j

    def get_file_type(file_name):
      if file_name.split('.')[-1] in ['jpeg', 'jpg', 'png', 'gif', 'bmp', 'JPEG', 'JPG', 'PNG', 'GIF', 'BMP']:
        return 'image'
      else:
        return 'video'
    file_items = sorted(onlyfiles, cmp=numeric_compare)
    items_info = []
    i = 1
    for file_item in file_items:
      session_item = SessionItem.objects.filter(video_session=self, item_number = i).first()
      if session_item is None:
        session_item = SessionItem(**{
          'video_session_id' : self.id,
          'item_number' : i,
          'item_type' : get_file_type(file_item),
          'item_file' : None
        })
        session_item.save()
      i = i + 1

  @classmethod
  def user_category_sessions(cls, user_id, category_id):
    return cls.objects.filter(video_template__categories__id=category_id, user_id=user_id).all()

  @classmethod
  def user_parent_template_variation_sessions(cls, user_id, parent_template):
    print cls.objects.filter(user_id=user_id, video_template_id__in=get_values_array(parent_template.variations_with_self().values('id'), 'id')).query
    return cls.objects.filter(user_id=user_id, video_template_id__in=get_values_array(parent_template.variations_with_self().values('id'), 'id'))


  def render(self, category_id, template_id):
    import requests
    zipped_project_path = self.zip_the_project()
    files = {'zipped_project': open(zipped_project_path, 'rb')}
    r = requests.post("{}/{}/{}/{}".format(RENDERER_SERVER, 'render_process', category_id, template_id), files = files, data = {'category_id' : category_id, 'template_id' : template_id, 'video_session_id' : self.id})
    self.rendering_started = True
    self.save()

  def zip_the_project(self):
    if os.path.exists(self.project_dir() + ".zip"):
      os.remove(self.project_dir() + ".zip")
    os.chdir(self.extract_dir())
    return shutil.make_archive(self.project_dir(), format='zip', root_dir=self.project_dir())

  def pre_delete(self):
    # print "STARTED DELETING SESSION ITEMS"
    # self.session_items.all().delete()
    # print "END DELETING SESSION ITEMS"
    extract_dir_full_path = self.extract_dir(False)
    print "STARTED DELETING extract dir"
    shutil.rmtree(extract_dir_full_path)
    print "END DELETING extract dir"
    if self.final_video:
      if os.path.exists(self.final_video.path):
        print "STARTED DELETING final video"
        os.remove(self.final_video.path)
        print "END DELETING final video"



def post_save_for_video_session(sender, instance, **kwargs):
  prevent_callback = False
  try:
    prevent_callback = instance.prevent_callback
  except:
    pass
  if not prevent_callback:
    instance.add_session_items()

def pre_delete_for_video_session(sender, instance, **kwargs):
  instance.pre_delete()

pre_delete.connect(pre_delete_for_video_session, sender = VideoSession)
post_save.connect(post_save_for_video_session, sender=VideoSession)

def session_item_relative_upload_path(instance, filename):
  return os.path.join(instance.video_session.footage_item_dir(True), filename)

def session_item_absolute_upload_path(instance, filename):
  return os.path.join(instance.video_session.footage_item_dir(False), filename)

def media_relative_path(path):
  return path.replace(MEDIA_ROOT + "/", '')

class SessionItem(models.Model):
  video_session = models.ForeignKey(VideoSession, related_name='session_items')
  item_number = models.IntegerField()
  item_type = models.CharField(max_length=100, choices=(('image','image'),('video','video')))
  item_file = models.FileField(upload_to=session_item_relative_upload_path, null = True, blank = True)

  def get_temp_files_path(self):
    temp_dir_name = os.path.join(self.video_session.extract_dir(False), "temp")
    if self.item_type == "image":
      return [os.path.join(temp_dir_name, self.item_file.path.split("/")[-1])]
    else:
      mp4_path = os.path.join(temp_dir_name, self.item_file.path.split("/")[-1]);
      webm_path = os.path.join(temp_dir_name, self.webm_path().split("/")[-1])
      return [mp4_path, webm_path]

  def webm_path(self):
    if self.item_type == "video" and self.item_file:
      mp4_path = self.item_file.path
      webm_path = self.item_file.path.split(".")
      webm_path[-1] = "webm"
      webm_path = ".".join(webm_path)
      return webm_path
    else:
      return None

  def delete_webm_file(self):
    if os.path.exists(self.webm_path()):
      os.remove(self.webm_path())

  def delete_item_file(self):
    if self.item_file:
      if self.item_type == "image":
        if os.path.exists(self.item_file.path):
          os.remove(self.item_file.path)
      else:
        mp4_path = self.item_file.path
        webm_path = self.webm_path()
        if os.path.exists(webm_path):
          os.remove(webm_path)


  def replace_from_temp(self, file_name_number):
    temp_dir_name = os.path.join(self.video_session.extract_dir(False), "temp")
    if self.item_type == "image":
      temp_file_path = os.path.join(temp_dir_name, "{}.{}".format(file_name_number, "jpeg"))
      if self.item_file and os.path.exists(self.item_file.path):
        orig_file_path = self.item_file.path
        os.remove(orig_file_path)
      else:
        orig_file_path = os.path.join(self.video_session.footage_item_dir(False), "{}.{}".format(self.item_number, "jpeg"))
      shutil.copyfile(temp_file_path, orig_file_path)
      self.item_file = orig_file_path.split("media/")[-1]
      self.prevent_callback = True
      self.save()
    else:
      mp4_temp_file_path = os.path.join(temp_dir_name, "{}.{}".format(file_name_number, "mp4"))
      webm_temp_file_path = os.path.join(temp_dir_name, "{}.{}".format(file_name_number, "webm"))
      if self.item_file and os.path.exists(self.item_file.path):
        orig_mp4_file_path = self.item_file.path
        os.remove(orig_mp4_file_path)
        orig_webm_file_path = self.webm_path()
        os.remove(orig_webm_file_path)
      else:
        orig_mp4_file_path = os.path.join(self.video_session.footage_item_dir(False), "{}.{}".format(self.item_number, "mp4"))
        orig_webm_file_path = os.path.join(self.video_session.footage_item_dir(False), "{}.{}".format(self.item_number, "webm"))
      shutil.copyfile(mp4_temp_file_path, orig_mp4_file_path)
      shutil.copyfile(webm_temp_file_path, orig_webm_file_path)
      self.item_file = orig_mp4_file_path.split("media/")[-1]
      self.prevent_callback = True
      self.save()


  def save_item_file(self, base64str):
    import base64
    import cStringIO
    from django.core.files.uploadedfile import InMemoryUploadedFile
    ext = ''
    content_type = ''
    extra_data = ''

    #delete previous file
    if self.item_file and os.path.exists(self.item_file.path):
      self.delete_item_file()

    if self.item_type == "image":
      if base64str.startswith('data:image/png;base64,'):
        ext = 'png'
        content_type = 'image/png'
        extra_data = 'data:image/png;base64,'
      elif base64str.startswith('data:image/jpeg;base64,'):
        ext = 'jpeg'
        content_type = 'image/jpeg'
        extra_data = 'data:image/jpeg;base64,'
    elif self.item_type == "video":
      if base64str.startswith('data:video/mp4;base64,'):
        ext = 'mp4'
        content_type = 'video/mp4'
        extra_data = 'data:video/mp4;base64,'
      elif base64str.startswith('data:video/mpeg;base64,'):
        ext = 'mpeg'
        content_type = 'video/mpeg'
        extra_data = 'data:video/mpeg;base64,'
      elif base64str.startswith('data:video/webm;base64,'):
        ext = 'webm'
        content_type = 'video/webm'
        extra_data = 'data:video/webm;base64,'
    base64str = base64str.replace(extra_data,'')
    base64str = base64str.replace(" ", "+")
    base64str_decoded = base64.b64decode(base64str)
    file = cStringIO.StringIO(base64str_decoded)
    uploaded_file = InMemoryUploadedFile(file,
      field_name='item_file',
      name=".".join([str(self.item_number), ext]),
      content_type=content_type,
      size=len(file.getvalue()),
      charset=None
    )

    #checking if the file exists as it was previously extracted from archive and then removing it
    if os.path.exists(session_item_absolute_upload_path(self, ".".join([str(self.item_number), ext]))):
      os.remove(session_item_absolute_upload_path(self, ".".join([str(self.item_number), ext])))
    self.item_file = uploaded_file
    self.save()

  def handle_file_conversions(self):
    if self.item_file and os.path.exists(self.item_file.path):
      ext = self.item_file.path.split('.')[-1]
      if self.item_type == 'image':
        if ext != 'jpeg':
          file_path_splitted = self.item_file.path.split('.')
          if ext == 'jpg':
            file_path_splitted[-1] = 'jpeg'
            new_file_path = '.'.join(file_path_splitted)
            os.rename(self.item_file.path, new_file_path)
            self.item_file = media_relative_path(new_file_path)
            self.save()
          elif ext == 'png':
            new_file_path = convert_png_to_jpeg(self.item_file.path)
            os.remove(self.item_file.path)
            self.item_file = media_relative_path(new_file_path)
            self.save()
        else:
          new_file_path = self.item_file.path
        new_file = open(new_file_path)
        image_generator = MainImageVariation(source=self.item_file)
        result = image_generator.generate()
        os.remove(new_file_path)
        destination = open(new_file_path, 'w')
        destination.write(result.read())
        destination.close()
      else:
        if ext != 'mp4':
          if ext == 'flv':
            new_file_path = convert_video(self.item_file.path, 'flv', 'mp4')
            os.remove(self.item_file.path)
            convert_video(new_file_path, 'mp4', 'webm')
            self.item_file = media_relative_path(new_file_path)
            self.prevent_callback = True
            self.save()

          elif ext == 'avi':
            new_file_path = convert_video(self.item_file.path, 'avi', 'mp4')
            os.remove(self.item_file.path)
            convert_video(new_file_path, 'mp4', 'webm')
            self.item_file = media_relative_path(new_file_path)
            self.prevent_callback = True
            self.save()

          elif ext == 'mpeg' or ext == 'mpg':
            new_file_path = convert_video(self.item_file.path, 'mpeg', 'mp4')
            os.remove(self.item_file.path)
            convert_video(new_file_path, 'mp4', 'webm')
            self.item_file = media_relative_path(new_file_path)
            self.prevent_callback = True
            self.save()

          elif ext == 'wmv':
            new_file_path = convert_video(self.item_file.path, 'wmv', 'mp4')
            os.remove(self.item_file.path)
            convert_video(new_file_path, 'mp4', 'webm')
            self.item_file = media_relative_path(new_file_path)
            self.prevent_callback = True
            self.save()
          elif ext == 'webm':
            new_file_path = convert_video(self.item_file.path, 'webm', 'mp4')
            self.item_file = media_relative_path(new_file_path)
            self.prevent_callback = True
            self.save()
        else:
          webm_path = self.webm_path()
          if webm_path is not None and not os.path.exists(self.webm_path()):
            convert_video(self.item_file.path, 'mp4', 'webm')


def post_save_for_session_item(sender, instance, **kwargs):
  prevent_callback = False
  try:
    prevent_callback = instance.prevent_callback
  except:
    pass
  if not prevent_callback:
    instance.handle_file_conversions()

def pre_delete_for_session_item(sender, instance, **kwargs):
  print "STARTED DELETING ITEM FILE FOR FILE NUMBER : " + str(instance.item_number)
  instance.delete_item_file()
  print "END DELETING ITEM FILE FOR FILE NUMBER : " + str(instance.item_number)

post_save.connect(post_save_for_session_item, sender=SessionItem)
pre_delete.connect(pre_delete_for_session_item, sender = SessionItem)

def convert_png_to_jpeg(path):
  convert_path = path.split('.')
  convert_path[-1] = 'jpeg'
  convert_path = ".".join(convert_path)
  process([
    'ffmpeg',
    '-i',
    path,
    convert_path
  ])
  return convert_path

def convert_video(path, source_format, destination_format):
  convert_path = path.split('.')
  process_params = []
  if source_format == 'mp4' and destination_format == 'webm':
    convert_path[-1] = 'webm'
    convert_path = ".".join(convert_path)
    process_params = [
      "ffmpeg",
      "-i",
      path,
      "-acodec",
      "libvorbis",
      "-aq",
      "5",
      "-ac",
      "2",
      "-qmax",
      "25",
      "-threads",
      "2",
      convert_path
    ]
  elif destination_format == 'mp4':
    convert_path[-1] = 'mp4'
    convert_path = ".".join(convert_path)
    if os.path.exists(convert_path):
      os.remove(convert_path)
    elif source_format == 'webm':
      convert_path[-1] = 'mp4'
      convert_path = ".".join(convert_path)
      process_params = [
        "ffmpeg",
        "-i",
        path,
        "-qscale",
        "0",
        convert_path
      ]
    if source_format == 'flv':
      process_params = ["ffmpeg",
        "-i",
        path,
        "-c:v",
        "libx264",
        "-crf",
        "19",
        "-strict",
        "experimental",
        convert_path
      ]
    elif source_format == 'avi':
      process_params = [
        "ffmpeg",
        "-i",
        path,
        "-c:v",
        "libx264",
        "-crf",
        "19",
        "-preset",
        "slow",
        "-c:a",
        "libfaac",
        "-b:a",
        "192k",
        "-ac",
        "2",
        convert_path
      ]
    elif (source_format == 'mpeg' or source_format == 'mpg'):
      process_params = [
        "ffmpeg",
        "-i",
        path,
        "-vcodec",
        "libx264",
        "-crf",
        "15",
        "-s",
        "640x480",
        "-aspect",
        "640:480",
        "-r",
        "30",
        "-threads",
        "4",
        "-acodec",
        "libvo_aacenc",
        "-ab",
        "128k",
        "-ar",
        "32000",
        "-async",
        "32000",
        "-ac",
        "2",
        "-scodec",
        "copy",
        convert_path
      ]
    elif source_format == 'wmv':
      process_params = [
        "ffmpeg",
        "-i",
        path,
        "-c:v",
        "libx264",
        "-crf",
        "23",
        "-c:a",
        "libfaac",
        "-q:a",
        "100",
        convert_path
      ]
  process(process_params)
  return convert_path


class Steaker(models.Model):
  title = models.CharField(max_length=1000, null=False, blank = False)
  image = models.ImageField(upload_to="steakers", null = False, blank = False)


def get_values_array(items, key):
  from operator import itemgetter
  return map(itemgetter(key), items)