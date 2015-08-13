from django.http import HttpResponseRedirect
from lib.classes import FlashedRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
def anonymous_only(action):
  def inner_func(*args, **kwargs):
    request = args[0]
    if not request.user.is_anonymous():
      if request.user.is_superuser:
        return HttpResponseRedirect(reverse('admins:dashboard'))
      else:
        return HttpResponseRedirect(reverse('yatra:categories'))
    return action(*args, **kwargs)
  return inner_func

def post(action):
  def inner_func(*args, **kwargs):
    request = args[0]
    if request.method != 'POST':
      return HttpResponseRedirect(reverse('yatra:home'))
    return action(*args, **kwargs)
  return inner_func

def flashable(action):
  def inner_func(*args, **kwargs):
    request = args[0]
    if 'flash_data' in request.session:
      request.flash_data = request.session['flash_data']
      del request.session['flash_data']
    if 'form' in request.session:
      request.form = request.session['form']
      del request.session['form']
    return action(*args, **kwargs)
  return inner_func

def admin_only(action):
  def inner_func(*args, **kwargs):
    request = args[0]
    if not request.user.is_superuser:
      if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('yatra:home'))
      else:
        return HttpResponseRedirect(reverse('admins:signin'))
    return action(*args, **kwargs)
  return inner_func

def token_user_only(action):
  def inner_func(*args, **kwargs):
    request = args[0]
    if request.user.is_anonymous():
      return FlashedRedirect(reverse('accounts:signin'), request, {
        'status' : 'error',
        'message' : 'Please sign in'
      })
    else:
      try:
        request.session['usage_token']
      except:
        logout(request)
        return FlashedRedirect(reverse('accounts:signin'), request, {
            'status' : 'error',
            'message' : 'Contact Administrator to get you a registration token, then register'
        })
    return action(*args, **kwargs)
  return inner_func


