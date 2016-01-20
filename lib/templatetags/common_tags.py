from django import template

register = template.Library()

@register.filter('get_template_category_names')
def get_template_category_names(template, separator):
  return ' '.join(map(lambda x: x['title'].lower(), template.categories.values('title')))


@register.filter('grouped_in')
def grouped_in(arr, n):
  print arr
  for i in xrange(0, len(arr), n):
    yield arr[i:i+n]

@register.filter('get_dom_id')
def get_dom_id(model_obj):
  return "{}_{}".format(type(model_obj).__name__.lower(), model_obj.id)