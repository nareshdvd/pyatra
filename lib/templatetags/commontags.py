import os
from django import template
from datetime import datetime
from pyatra.settings import *
from PIL import Image
register = template.Library()
import time

@register.filter(name="curr_timestamp")
def curr_timestamp(teststr):
  return int(time.time())

@register.filter(name="increment_by")
def increment_by(num, increase_by):
  return num + increase_by


@register.filter(name="formated")
def formated(timestamp, format):
  return datetime.fromtimestamp(float(timestamp)).strftime(format)

@register.filter(name="get_ogg_path")
def get_ogg_path(path):
  return path.replace(".mp4", ".ogg")


@register.filter(name="get_image_from_list")
def get_image_from_list(images, index):
  try:
    return images[index - 1]
  except:
    return ''

@register.filter(name="get_image_width")
def get_image_width(images, index):
  try:
    file_path = '{}/{}'.format(BASE_DIR, images[index - 1])
    im=Image.open(file_path)
    return im.size[0]
  except:
    return 0

@register.filter(name="get_image_height")
def get_image_height(images, index):
  try:
    file_path = '{}/{}'.format(BASE_DIR, images[index - 1])
    im=Image.open(file_path)
    return im.size[1]
  except:
    return 0

@register.filter(name="get_view_template_partial_path")
def get_view_template_partial_path(video_templates):
  # if video_templates.count() in [1,2,3]:
  #   return 'video_template_partials/{}.html'.format(str(video_templates.count()))
  # else:
  return 'video_template_partials/more.html'

@register.filter(name="grouped_in")
def grouped_in(collection, group_count):
  total =  len(collection)
  num_rows = total / group_count
  if (num_rows * group_count) < total:
    num_rows = num_rows + 1
  groups = []
  prev = 0
  for k in range(group_count, total, group_count):
    groups.append(collection[prev:k])
    # range(prev, k)
    prev = k
  if len(groups) < num_rows:
    groups.append(collection[prev:total])
  return groups



@register.filter(name="in_array")
def in_array(element, array):
  if array.__class__.__name__ == 'list':
    if str(element) in array:
      return True
    else:
      return False
  else:
    return False

@register.filter(name="get_ordered_item")
def get_ordered_item(items, order):
  item = items.filter(content_order=order).first()
  if item is not None:
    return item
  else:
    return False

@register.filter(name="timestamp")
def timestamp(tmpstr):
  import time
  return str(int(time.time()))

@register.filter(name="get_resized")
def get_resized(yatra_content, size):
  return yatra_content.resized(size)

@register.filter(name="get_first_n_items")
def get_first_n_items(items, n):
  return items[0:n]

@register.filter(name="get_all_items_from_n")
def get_all_items_from_n(items, n):
  items_count = len(items)
  if(items_count == n):
    return []
  else:
    return items[n:items_count]

@register.filter(name="get_format_path")
def get_format_path(input_file_path, io_format):
  formats = io_format.split(':')
  input_format = formats[0]
  output_format = formats[1]
  return input_file_path.replace(input_format, output_format)