from django.conf.urls import include, url
from admins import views
from admins import usage_tokens
from admins import video_templates
from admins import template_categories

urlpatterns = [
  url(r'^signin$', views.signin, name='signin'),
  url(r'^signin/post$', views.signin_post, name='signin_post'),
  url(r'^signout$', views.signout, name='signout'),
  url(r'^dashboard$', views.dashboard, name='dashboard'),

  url(r'^usage_tokens$', usage_tokens.index, name='usage_tokens'),
  url(r'^usage_tokens/new$', usage_tokens.new, name='new_usage_token'),
  url(r'^usage_tokens/save$', usage_tokens.save, name='save_usage_token'),
  url(r'^usage_tokens/(?P<id>[0-9]+)/edit$', usage_tokens.edit, name='edit_usage_token'),
  url(r'^usage_tokens/(?P<id>[0-9]+)/update$', usage_tokens.update, name='update_usage_token'),
  url(r'^usage_tokens/(?P<id>[0-9]+)/delete$', usage_tokens.delete, name='delete_usage_token'),


  url(r'^video_templates$', video_templates.index, name='video_templates'),
  url(r'^video_templates/new$', video_templates.new, name='new_video_template'),
  url(r'^video_templates/save$', video_templates.save, name='save_video_template'),
  url(r'^video_templates/(?P<id>[0-9]+)/edit$', video_templates.edit, name='edit_video_template'),
  url(r'^video_templates/(?P<id>[0-9]+)/update$', video_templates.update, name='update_video_template'),
  url(r'^video_templates/(?P<id>[0-9]+)/delete$', video_templates.delete, name='delete_video_template'),


  url(r'^template_categories$', template_categories.index, name='template_categories'),
  url(r'^template_categories/new$', template_categories.new, name='new_template_category'),
  url(r'^template_categories/save$', template_categories.save, name='save_template_category'),
  url(r'^template_categories/(?P<id>[0-9]+)/edit$', template_categories.edit, name='edit_template_category'),
  url(r'^template_categories/(?P<id>[0-9]+)/update$', template_categories.update, name='update_template_category'),
  url(r'^template_categories/(?P<id>[0-9]+)/delete$', template_categories.delete, name='delete_template_category'),
]