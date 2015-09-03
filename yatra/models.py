from django.db import models
from django.contrib.auth.models import User
from lib.classes import FileHandler
from PIL import Image, ImageOps
import uuid
import os

class Category(models.Model):
  title = models.CharField(max_length=500)
  description = models.TextField(null=True, blank=True, default='')
  cover_image = models.ImageField(upload_to='category_images')

  def resized(self, width_height):
    resized_dir = os.path.join(MEDIA_ROOT, 'category_images', 'resized')
    if not os.path.exists(resized_dir):
      os.mkdir(resized_dir)

    resized_path = os.path.join(MEDIA_ROOT, 'category_images', 'resized', '{}_{}.{}'.format(self.id, width_height, 'jpeg'))
    resized_url = '/media/{}/resized/{}_{}.{}'.format('category_images', self.id, width_height, 'jpeg')
    if os.path.exists(resized_path):
      os.remove(resized_path)
    path = self.cover_image.path
    width = int(width_height.split('X')[0])
    height = int(width_height.split('X')[1])
    image = Image.open(path)
    if image.mode not in ("L", "RGB"):
      image = image.convert("RGB")
    image = image.resize((width,height), Image.ANTIALIAS)
    image.save(resized_path, "jpeg", quality=90)
    return resized_url

class Template(models.Model):
  title = models.CharField(max_length=500)
  demo_file = models.FileField(upload_to='template_demo_videos')
  project_compressed_file = models.FileField(upload_to='zipped_projects')
  categories = models.ManyToManyField(Category, related_name='category_templates')
  item_positions = models.TextField(null=True, blank=True, default='')
  variation_id = models.CharField(max_length=100, null=True, blank=True, default=None)
  main_variation = models.BooleanField(blank=True, default=False)
  variation_description = models.TextField(null=True, blank=True, default=None)

  #if variation_id is None a new random variation_id is generated otherwise given variation_id is used, so that a relation can be maintained within variations of same template
  @classmethod
  def create_new(cls, variation_id=None):
    main_variation = False
    if variation_id == None:
      variation_id=uuid.uuid4()
      main_variation = True
    template = Template()
    template.variation_id=variation_id
    template.main_variation = main_variation
    return template


  @classmethod
  def add(cls, post_data):
    demo_file = post_data['demo_file']
    extension = FileHandler.get_extension(demo_file)
    file_name = '{}.{}'.format(uuid.uuid4(), extension)
    demo_file_path = 'template_demo_videos/{}'.format(file_name)
    FileHandler.uploadfile(demo_file, demo_file_path)

    project_compressed_file = post_data['project_compressed_file']
    extension = FileHandler.get_extension(project_compressed_file)
    file_name = '{}.{}'.format(uuid.uuid4(), extension)
    project_compressed_file_path = 'zipped_projects/{}'.format(file_name)
    FileHandler.uploadfile(project_compressed_file, project_compressed_file_path)

    object = cls(**{
      'title' : post_data['title'],
      'demo_file' : demo_file_path,
      'project_compressed_file' : project_compressed_file_path,
      'variation_id' : post_data['variation_id']
    })

    # print post_data
    # print post_data['variation_id']
    # print object.variation_id
    # return
    if 'variation_description' in post_data.keys():
      object.variation_description = post_data['variation_description']

    if 'main_variation' in post_data.keys():
      if post_data['main_variation'] == 'True' or post_data['main_variation'] == True or post_data['main_variation'] == '1' or post_data['main_variation'] == 1:
        object.main_variation = True
      else:
        object.main_variation = False
    object.save()
    # object.save_ogg_file()
    for cid in post_data['categories']:
      object.categories.add(Category.objects.get(pk=cid))
    return object

  def get_main_variation(self):
    if self.main_variation == True:
      return self
    else:
      return Template.objects.filter(variation_id=self.variation_id, main_variation=True).first()

  @classmethod
  def update(cls, post_data):
    object = cls.objects.get(pk=post_data['id'])
    object.title = post_data['title']
    object.variation_description = post_data['variation_description']
    if 'demo_file' in post_data.keys() and post_data['demo_file'] != '' and post_data['demo_file'] != None:
      demo_file = post_data['demo_file']
      extension = FileHandler.get_extension(demo_file)
      file_name = '{}.{}'.format(uuid.uuid4(), extension)
      demo_file_path = 'template_demo_videos/{}'.format(file_name)
      FileHandler.uploadfile(demo_file, demo_file_path)
      object.demo_file = demo_file_path

    if 'project_compressed_file' in post_data.keys() and post_data['project_compressed_file'] != '' and post_data['project_compressed_file'] != None:
      project_compressed_file = post_data['project_compressed_file']
      extension = FileHandler.get_extension(project_compressed_file)
      file_name = '{}.{}'.format(uuid.uuid4(), extension)
      project_compressed_file_path = 'zipped_projects/{}'.format(file_name)
      FileHandler.uploadfile(project_compressed_file, project_compressed_file_path)
      object.project_compressed_file = project_compressed_file_path

    object.save()

    old_categories = [obj.id for obj in object.categories.all()]
    for ocategory in old_categories:
      if ocategory not in post_data['categories']:
        object.categories.remove(Category.objects.get(pk=ocategory))

    for cid in post_data['categories']:
      if cid not in old_categories:
        object.categories.add(Category.objects.get(pk=cid))
    return object





  def remove(self):
    try:
      demo_file_path = self.demo_file.path
      if demo_file_path.endswith('.mp4'):
        ogg_path = demo_file_path.replace('.mp4','.ogg')
      elif demo_file_path.endswith('.flv'):
        ogg_path = demo_file_path.replace('.flv','.ogg')
      os.remove(demo_file_path)
      try:
        os.remove(ogg_path)
      except:
        pass
    except:
      pass

    try:
      project_compressed_file_path = self.project_compressed_file.path
      os.remove(project_compressed_file_path)
    except:
      pass
    for video_session in self.template_video_sessions.all():
      video_session.remove()
    self.delete()

  def extract(self, video_session):
    zipped_file_name = self.project_compressed_file.path.split('/')
    zipped_file_name = zipped_file_name[len(zipped_file_name)-1]
    extracted_dir = os.path.join(MEDIA_ROOT, 'user_extracted_projects', video_session.session_id)
    if os.path.exists(extracted_dir):
      shutil.rmtree(extracted_dir)
    os.mkdir(extracted_dir)

    if zipped_file_name.endswith('.zip'):
      process([
        'unzip',
        self.project_compressed_file.path,
        '-d',
        extracted_dir
      ])
      extension = '.zip'
    elif zipped_file_name.endswith('.tar'):
      process([
        'tar',
        '-zxvf',
        self.project_compressed_file.path,
        '-C',
        extracted_dir
      ])
      extension = '.tar'

    uncompressed_project_dir = [x[0] for x in os.walk(extracted_dir)][1]
    uncompressed_project_dir_name = uncompressed_project_dir.split('/')
    uncompressed_project_dir_name = uncompressed_project_dir_name[len(uncompressed_project_dir_name) - 1]
    new_uncompressed_project_dir = uncompressed_project_dir.replace(uncompressed_project_dir_name, zipped_file_name.replace(extension, ''))
    process([
      'mv',
      uncompressed_project_dir,
      new_uncompressed_project_dir
    ])
    return new_uncompressed_project_dir

  def render(self, video_session):
    extracted_project_dir = self.extract(video_session)
    template_project_file_path = os.path.join(extracted_project_dir, 'template.aep')
    output_path = os.path.join(MEDIA_ROOT, 'final_videos', video_session.session_id, 'output.mov')
    process([
      r'/Applications/Adobe After Effects CC 2014/aerender',
      '-project',
      template_project_file_path,
      '-comp',
      'final_comp',
      '-mp',
      '-output',
      output_path
    ])

  def set_items_info(self):
    path = self.project_compressed_file.path
    extract_dir = MEDIA_ROOT
    while os.path.exists(extract_dir):
      random_dir = str(random.randint(10000000000, 99999999999))
      extract_dir = os.path.join(MEDIA_ROOT, 'temp_video_templates', random_dir)
    os.makedirs(extract_dir)
    if self.is_zipped():
      process([
        'unzip',
        self.project_compressed_file.path,
        '-d',
        extract_dir
      ])
      extension = '.zip'
    elif self.is_tarred():
      process([
        'tar',
        '-zxvf',
        self.project_compressed_file.path,
        '-C',
        extract_dir
      ])
      extension = '.tar'

    uncompressed_project_dir = [x[0] for x in os.walk(extract_dir)][1]
    footage_items_dir = os.path.join(uncompressed_project_dir, 'footage_items')


    onlyfiles = [ f for f in listdir(footage_items_dir) if isfile(join(footage_items_dir,f)) ]
    # files_count = len(onlyfiles)
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
    i = 0
    for file_item in file_items:
      tmp_path = '{}/{}'.format(footage_items_dir, file_item)
      tmp_path = tmp_path.replace(BASE_DIR, '')
      items_info.append({
        'file_name' : file_item.split('.')[0],
        'extension' : file_item.split('.')[1],
        'file_type' : get_file_type(file_item),
        'tmp_path' : tmp_path
      })
      i = i + 1
    self.item_positions = json.dumps(items_info)
    self.save()

  def get_items_info(self):
    if self.item_positions is None or self.item_positions == '':
      self.set_items_info()
    return json.loads(self.item_positions)

  def is_zipped(self):
    return self.project_compressed_file.path.endswith(".zip")

  def is_tarred(self):
    return self.project_compressed_file.path.endswith(".tar")


class VideoSession(models.Model):
  session_id = models.CharField(max_length=255)
  user = models.ForeignKey(User, related_name='video_sessions')
  video_template = models.ForeignKey(Template, related_name='template_video_sessions')
  timestamp = models.CharField(max_length=255, blank=True, default='')
  video_generated = models.BooleanField(blank=True, default=False)
  video = models.FileField(upload_to='final_videos', null=True, blank=True)

  @classmethod
  def generate(cls, user, video_template):
    timestamp = str(time.time())
    session_id = str(uuid.uuid4())
    object = cls(**{
      'session_id' : session_id,
      'user_id' : user.id,
      'video_template_id' : video_template.id,
      'timestamp' : timestamp
    })
    object.save()
    return object

  @classmethod
  def get_or_generate(cls, user, video_template):
    try:
      object = cls.objects.get(user=user, video_template=video_template)
    except:
      object = cls.generate(user, video_template)
    return object

  def remove(self):
    try:
      os.remove(self.video.path)
    except:
      pass

    extracted_dir = os.path.join(MEDIA_ROOT, 'user_extracted_projects', self.session_id)
    if os.path.exists(extracted_dir):
      shutil.rmtree(extracted_dir)

    for content in self.contents.all():
      content.remove()
    self.delete()


  @property
  def viewablecontents(self):
    return self.contents.filter(Q(content_type='IMAGE')|Q(content_type='VIDEO')).order_by('content_order')

  def add_base64_photo(self, content_order, base64str):
    converted_image = convert_to_image(base64str)
    items_info = self.video_template.get_items_info()
    item_info = items_info[int(content_order)]
    extension = item_info['extension']
    file_path = FileHandler.get_video_session_file_path(self, content_order, extension)
    FileHandler.uploadbase64file(base64str, file_path)
    content_obj = self.viewablecontents.filter(content_order=content_order).first()
    if content_obj is None:
      photo_data['content_type'] = 'IMAGE'
      photo_data['video_session_id'] = self.id
      photo_data['attachment'] = file_path
      photo_data['content_order'] = content_order
      content_obj = YatraContent(**photo_data)
    content_obj.save()

  def add_photo(self, photo_data):
    attachment = photo_data['attachment']
    extension = FileHandler.get_extension(attachment)
    photo_data['content_type'] = 'IMAGE'
    photo_data['video_session_id'] = self.id
    photo = YatraContent(**photo_data)
    file_path = FileHandler.get_video_session_file_path(self, photo_data['content_order'], extension)
    FileHandler.uploadfile(attachment, file_path)
    photo_data['attachment'] = file_path
    photo = YatraContent(**photo_data)
    photo.save()
    photo.resize()
    return photo


  def add_video(self, video_data):
    attachment = video_data['attachment']
    extension = FileHandler.get_extension(attachment)
    video_data['content_type'] = 'VIDEO'
    video_data['video_session_id'] = self.id
    video = YatraContent(**video_data)
    file_path = FileHandler.get_video_session_file_path(self, video_data['content_order'], extension)
    FileHandler.uploadfile(attachment, file_path)
    video_data['attachment'] = file_path
    video = YatraContent(**video_data)
    video.save()
    return video

class YatraContent(models.Model):
  CONTENT_TYPE = (('IMAGE','IMAGE'), ('AUDIO','AUDIO'), ('VIDEO', 'VIDEO'))
  attachment = models.FileField(upload_to='uploads')
  video_session = models.ForeignKey(VideoSession, related_name='contents')
  content_type = models.CharField(max_length=10, choices=CONTENT_TYPE)
  content_order = models.IntegerField(blank=True, null=True, default=0)
  class Meta:
    verbose_name = 'Yatra Content'
    verbose_name_plural = 'Yarta Contents'

  @property
  def is_image(self):
    return self.content_type == 'IMAGE'

  @property
  def is_video(self):
    return self.content_type == 'VIDEO'



  def resized(self, width_height):
    resized_dir = os.path.join(MEDIA_ROOT, 'uploads', self.video_session.session_id, 'resized')
    if not os.path.exists(resized_dir):
      os.mkdir(resized_dir)

    resized_path = os.path.join(MEDIA_ROOT, 'uploads', self.video_session.session_id, 'resized', '{}_{}.{}'.format(self.content_order, width_height, 'jpeg'))
    resized_url = '/media/uploads/{}/resized/{}_{}.{}'.format(self.video_session.session_id, self.content_order, width_height, 'jpeg')
    if os.path.exists(resized_path):
      os.remove(resized_path)

    if self.content_type == "IMAGE":
      width = int(width_height.split('X')[0])
      height = int(width_height.split('X')[1])
      path = self.attachment.path
      image = Image.open(path)
      # tmppath = '/tmp/' + path.replace('/','_')

      if image.mode not in ("L", "RGB"):
        image = image.convert("RGB")
      image = image.resize((width,height), Image.ANTIALIAS)
      image.save(resized_path, "jpeg", quality=90)
      return resized_url
    else:
      return self.attachment.url


  def resize(self):
    if self.content_type == "IMAGE":
      path = self.attachment.path
      image = Image.open(path)
      tmppath = '/tmp/' + path.replace('/','_')
      if image.mode not in ("L", "RGB"):
        image = image.convert("RGB")
      image = image.resize((1920,1080), Image.ANTIALIAS)
      image.save(tmppath, "jpeg", quality=75)
      os.remove(path)
      shutil.copyfile(tmppath, path)
      os.remove(tmppath)
    # else:
    #   path = self.attachment.path
    #   tmppath = '/tmp/' + path.replace('/','_')
    #   process(['ffmpeg', '-i', path, '-vf', 'scale=1920:1080', tmppath])
    #   os.remove(path)
    #   shutil.copyfile(tmppath, path)
    #   os.remove(tmppath)

  def remove(self):
    try:
      path = self.attachment.path
      os.remove(path)
    except:
      pass
    self.delete()


