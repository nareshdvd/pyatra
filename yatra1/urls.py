from django.conf.urls import include, url
from yatra import views

urlpatterns = [
  url(r'^$', views.home, name='home'),
  url(r'^categories$', views.categories, name="categories"),
  url(r'^select/category/(?P<id>[0-9]+)$', views.select_category, name='select_category_post'),
  url(r'^templates$', views.templates, name="templates"),
  url(r'^(?P<category_id>[0-9]+)/select/template/(?P<id>[0-9]+)$', views.select_template, name="select_template_post"),
  url(r'^items$', views.items, name="yatra_items"),
  url(r'^items/(?P<item_number>[0-9]+)$', views.get_item, name="get_item"),
  url(r'^item/(?P<item_number>[0-9]+)/upload/form$', views.show_upload, name="show_upload"),
  url(r'^item/(?P<item_number>[0-9]+)/save_modified$', views.save_modified_image, name="save_modified_image"),
  url(r'^items/(?P<item_number>[0-9]+)/crop$', views.get_item_crop, name="get_item_crop"),
  url(r'^items/(?P<item_number>[0-9]+)/save_crop$', views.post_item_crop, name="post_item_crop"),
  url(r'^items/save$', views.save_item, name="save_item"),
  url(r'^test$', views.test, name="test")
]