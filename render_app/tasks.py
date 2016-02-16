from pyatra import celery_app
from render_app.lib import process
from render_app import after_finished_tasks


@celery_app.task
def delayed_process(params):
  next_process_params = None
  next_delayed_process_params = None
  after_finished_task = None
  after_finished_task_params = []
  print params
  if type(params[-1]) == dict:
    extra_params = params[-1]
    del params[-1]
    try:
      process(params)
    except:
      if 'on_error_task' in extra_params.keys():
        getattr(after_finished_tasks, extra_params['on_error_task']['name'])
      process(params)
    if ('next_process_params' in extra_params.keys()):
      next_process_params = extra_params['next_process_params']
    if ('next_delayed_process_params' in extra_params.keys()):
      next_delayed_process_params = extra_params['next_delayed_process_params']
    if ('after_finished_task' in extra_params.keys()):
      after_finished_task = extra_params['after_finished_task']
      task_name = after_finished_task['name']
      task_params = after_finished_task['params']
      result = getattr(after_finished_tasks, task_name)(*task_params)
  else:
    try:
      process(params)
    except:
      process(params)
  if next_process_params is not None:
    process(next_process_params)
  print "BELOW  IS  THE  VALUE  OF  NEXT  delayed process params"
  print next_delayed_process_params
  if next_delayed_process_params is not None:
    delayed_process.delay(next_delayed_process_params)
  return True