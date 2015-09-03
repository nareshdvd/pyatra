from django import template
register = template.Library()

@register.filter(name="get_categoriy_ids_array")
def get_categoriy_ids_array(object):
  categories = []
  try:
    category_objs = object.categories.all()
    for cate_obj in category_objs:
      categories.append(str(cate_obj.id))
  except:
    pass
  return categories

@register.filter(name="skip_first")
def skip_first(obj_array):
  return obj_array[1:len(obj_array)]