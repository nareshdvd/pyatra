from __future__ import unicode_literals

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
import subprocess
from subprocess import Popen
from django.db.models.signals import post_save
from pyatra.settings import MEDIA_ROOT
import os
from os import listdir
import shutil
from os.path import isfile, join
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
    from itertools import chain
    variations = self.variations.all()
    return list(chain([self], variations))

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


class VideoSession(models.Model):
  session_id = models.CharField(max_length = 255, null = False, blank = False)
  user = models.ForeignKey(User, related_name = 'video_sessions')
  video_template = models.ForeignKey(VideoTemplate, related_name = 'video_session')
  final_video = models.CharField(max_length=2000, null = True, blank = True, default = '')

  @classmethod
  def new_session(cls, user, video_template):
    import uuid
    video_session = VideoSession.objects.filter(user=user, video_template=video_template).first()
    if video_session is None:
      video_session = VideoSession(**{
          'session_id' : str(uuid.uuid4()),
          'user_id' : user.id,
          'video_template_id' : video_template.id
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

  def add_session_items(self):
    self.extract_project()
    footage_items_dir = self.footage_item_dir(False)
    onlyfiles = [ f for f in listdir(footage_items_dir) if (isfile(join(footage_items_dir,f)) and unicode(f.split('/')[-1].split('.')[0]).isnumeric()) ]
    def numeric_compare(i, j):
      i = int(i.split('.')[0])
      j = int(j.split('.')[0])
      return i - j

    def get_file_type(file_name):
      if file_name.split('.')[1] in ['jpeg', 'jpg', 'png', 'gif', 'bmp', 'JPEG', 'JPG', 'PNG', 'GIF', 'BMP']:
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
          'item_type' : file_item.split('.')[-1],
          'item_file' : None
        })
        session_item.save()
      i = i + 1

  def render():
    pass



def post_save_for_video_session(sender, instance, **kwargs):
  instance.add_session_items()


post_save.connect(post_save_for_video_session, sender=VideoSession)

def upload_dir(instance, filename):
  return os.path.join(instance.video_session.extract_dir(True), 'footage_items')

class SessionItem(models.Model):
  video_session = models.ForeignKey(VideoSession, related_name='session_items')
  item_number = models.IntegerField()
  item_type = models.CharField(max_length=100, choices=(('image','image'),('video','video')))
  item_file = models.FileField(upload_to=upload_dir, null = True, blank = True)

  def handle_file_conversions(self):
    if bool(self.item_file.name) is not False:
      ext = self.item_file.path.split('.')[-1]
      if self.item_type == 'image':
        if ext != 'jpeg':
          file_path_splitted = self.item_file.path.split('.')
          if ext == 'jpg':
            file_path_splitted[-1] = 'jpeg'
            new_file_path = file_path_splitted.join('.')
            os.rename(self.item_file.path, new_file_path)
          elif ext == 'png':
            convert_png_to_jpeg(self.item_file.path)
      else:
        if ext != 'flv':
          if ext == 'mp4':
            convert_video(self.item_file.path, 'mp4', 'flv')
          elif ext == 'avi':
            convert_video(self.item_file.path, 'avi', 'flv')
          elif ext == 'mpeg' or ext == 'mpg':
            convert_video(self.item_file.path, 'mpeg', 'flv')
          elif ext == 'wmv':
            convert_video(self.item_file.path, 'wmv', 'flv')

def post_save_for_session_item(sender, instance, **kwargs):
  instance.handle_file_conversions()

post_save.connect(post_save_for_session_item, sender=SessionItem)

    
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

def convert_video(path, source_format, destination_format):
  convert_path = path.split('.')
  convert_path[-1] = 'flv'
  convert_path = ".".join(convert_path)
  process_params = []
  if source_format == 'mp4':
    process_params = ["ffmpeg"
      ,"-i"
      ,path
      ,"-c:v"
      ,"libx264"
      ,"-ar"
      ,"22050"
      ,"-crf"
      ,"28"
      ,convert_path
    ]
  elif source_format == 'avi':
    process_params = [
      "ffmpeg", 
      "-i ",
      path,
      "-y",
      "-ab",
      "56",
      "-ar",
      "44100",
      "-b",
      "200k",
      "-r",
      "15",
      "-f",
      "flv",
      convert_path
    ]
  elif source_form == 'mpeg' or source_form == 'mpg':
    process_params = [
      "ffmpeg",
      "-i",
      path,
      "-deinterlace",
      "-ar",
      "44100",
      "-r",
      "25",
      "-qmin",
      "3",
      "-qmax",
      "6",
      convert_path
    ]
  elif source_form == 'wmv':
    process_params = [
      "ffmpeg",
      "-i",
      "path",
      "-ar",
      "44100",
      "-vcodec",
      "flv",
      "convert_path "
    ]
  process(process_params)


class Steaker(models.Model):
  title = models.CharField(max_length=1000, null=False, blank = False)
  image = models.ImageField(upload_to="steakers", null = False, blank = False)