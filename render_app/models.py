from django.db import models
import os
from pyatra.settings import MEDIA_ROOT, MAIN_SERVER
from render_app.lib import process as app_process
from render_app.tasks import delayed_process_for_render_process
from django.db.models.signals import post_save
import requests
import shutil
class RenderServer(models.Model):
  ip_address = models.CharField(max_length=100, blank=True, null=True)
  port = models.CharField(max_length=10, blank=True, null=True)

  def url(self, secured = False):
    return '{}//{}:{}'.format('https' if secured else 'http', self.ip_address, self.port)

  @classmethod
  def most_available(cls):
    import operator
    return cls.objects.get(pk=sorted({server.id : server.processes.count() for server in cls.objects.all()}.items(), key=operator.itemgetter(1))[0][0])

def render_project_upload_path(instance, filename):
  instance.main_dir()
  if os.path.exists(os.path.join(MEDIA_ROOT, str(instance.session_id), filename)):
    os.remove(os.path.join(MEDIA_ROOT, str(instance.session_id), filename))
  return os.path.join(str(instance.session_id), filename)
class RenderProcess(models.Model):
  P_STATE_CHOICES = (('',''), ('queued','queued'),('started','started'),('finished','finished'),('failed','failed'),)
  render_server = models.ForeignKey(RenderServer, related_name='processes')
  process_state = models.CharField(max_length=100, choices=P_STATE_CHOICES, default='')
  session_id = models.IntegerField()
  zipped_project = models.FileField(upload_to=render_project_upload_path)
  failed_count = models.IntegerField(default=0)

  def main_dir(self):
    m_dir = os.path.join(MEDIA_ROOT, str(self.session_id))
    if not os.path.exists(m_dir):
      os.mkdir(m_dir)
    return m_dir
    
  def dir_name(self):
    return self.zipped_project.path.split("/")[-1].replace(".zip","").replace(".tar","").replace(".gz", "")

  def extracted_dir_path(self):
    return os.path.join(self.main_dir(), self.dir_name())

  def template_file_path(self):
    return os.path.join(self.main_dir(), self.dir_name(), 'template.aep')

  def output_file_ext_path(self, ext):
    return os.path.join(self.main_dir(), 'output.{}'.format(ext))

  def is_zip_or_tar(self):
    if self.zipped_project.path.endswith('.zip'):
      return 'zip'
    else:
      return 'tar'

  def add_to_delayed_jobs(self):
    extract_to = self.extracted_dir_path()
    if os.path.exists(self.extracted_dir_path()):
      print "DELETING OLD EXTRACTED DIRECTORY"
      shutil.rmtree(self.extracted_dir_path())
    if self.is_zip_or_tar() == 'zip':
      app_process(['unzip', self.zipped_project.path, '-d', extract_to])
    else:
      app_process(['tar', '-zxvf', self.zipped_project.path, '-C', extract_to])
    delayed_process_for_render_process.delay(self, [r'/Applications/Adobe After Effects CC 2014/aerender', '-project', self.template_file_path(), '-comp', 'final_comp', '-mp', '-output', self.output_file_ext_path("mov")])

def post_save_for_render_process(sender, instance, **kwargs):
  try:
    if instance.previous_state == "started":
      if instance.process_state == "finished":
        app_process(['ffmpeg', '-i', instance.output_file_ext_path("mov"), '-q:a', '0', '-q:v', '0', instance.output_file_ext_path("mp4")])
        app_process(["ffmpeg", "-i", instance.output_file_ext_path("mp4"), "-acodec", "libvorbis", "-aq", "5", "-ac", "2", "-qmax", "25", "-threads", "2", instance.output_file_ext_path("webm")])
        files = {'output_file': open(instance.output_file_ext_path("mp4"), 'rb'), 'webm_file' : open(instance.output_file_ext_path('webm'), 'rb')}
        print "making request to" + "{}/{}/{}".format(MAIN_SERVER, 'render_finished', instance.session_id)
        r = requests.post("{}/{}/{}".format(MAIN_SERVER, 'render_finished', instance.session_id), files = files, data = {'video_session_id' : instance.session_id})
      elif instance.process_state == "failed" and instance.failed_count < 6:
        instance.add_to_delayed_jobs()
      elif instance.process_state == "failed" and instance.failed_count == 6:
        r = requests.post("{}/{}/{}".format(MAIN_SERVER, 'render_failed', instance.session_id))
  except:
    if instance.process_state == "":
      instance.add_to_delayed_jobs()

post_save.connect(post_save_for_render_process, sender=RenderProcess)
