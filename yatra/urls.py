from django.conf.urls import include, url
from yatra import views
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
  url(r'^$', views.home, name='home'),
  url(r'^categories$', views.view_categories, name="view_categories"),
  url(r'^categories/(?P<id>[0-9]+)/select$', views.select_category, name="select_category"),
  url(r'^templates$', views.view_templates, name="view_templates"),
  url(r'^templates/(?P<id>[0-9]+)/select$', views.select_template, name="select_template"),
  url(r'^templates/variations/(?P<variation_id>[0-9a-zA-Z_\-]+)$', views.view_variations, name="view_variations"),
  url(r'^items$', views.view_items, name="view_items"),
  url(r'items/(?P<item_number>[0-9]+)/edit', views.view_edit_item, name="view_edit_item"),
  url(r'items/(?P<item_number>[0-9]+)/upload', views.upload_item, name="upload_item"),
  url(r'items/(?P<item_number>[0-9]+)/save_modified', views.upload_base64_image_item, name="upload_base64_image_item"),
  url(r'items/(?P<item_number>[0-9]+)/save_cropped_image', views.save_cropped_image, name="save_cropped_image"),
  url(r'items/(?P<item_number>[0-9]+)/save_cropped_video', views.save_cropped_video, name="save_cropped_video"),
  url(r'render$', views.render, name='render'),
  url(r'receive_rendered_video$', csrf_exempt(views.receive_rendered_video), name='receive_rendered_video'),
  url(r'final_video$', views.final_video, name='final_video'),
]