from pyatra import celery_app
from render_app.lib import process

@celery_app.task
def delayed_process(params):
  process(params)
  return True