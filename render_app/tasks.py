from pyatra import celery_app
from render_app.lib import process
from render_app import after_finished_tasks


@celery_app.task
def delayed_process(params):
  next_process_params = None
  next_delayed_process_params = None
  after_finished_task = None
  after_finished_task_params = []
  if type(params[-1]) == dict:
    if ('next_process_params' in params[-1].keys()):
      next_process_params = params[-1]['next_process_params']
    if ('next_delayed_process_params' in params[-1].keys()):
      next_delayed_process_params = params[-1]['next_delayed_process_params']
    if ('after_finished_task' in params[-1].keys()):
      after_finished_task = params[-1]['after_finished_task']
      task_name = after_finished_task['name']
      task_params = after_finished_task['params']
      result = getattr(after_finished_tasks, task_name)(*task_params)
  process(params)
  if next_process_params is not None:
    process(next_process_params)

  if next_delayed_process_params is not None:
    delayed_process.delay(next_delayed_process_params)
  return True