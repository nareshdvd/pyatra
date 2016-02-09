"""pyatra URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
  https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
  1. Add an import:  from my_app import views
  2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
  1. Add an import:  from other_app.views import Home
  2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
  1. Add an import:  from blog import urls as blog_urls
  2. Import the include() function: from django.conf.urls import url, include
  3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
import yatra_app.views as yatra_app_views
import accounts.views as accounts_views
from django.conf import settings
from django.conf.urls.static import static
import render_app.views as render_app_views
urlpatterns = [
  url(r'^admin/', admin.site.urls),
  url(r'^$', yatra_app_views.home),
  url(r'^edit/(?P<id>[0-9]+)$', yatra_app_views.edit),
  url(r'^variations/(?P<category_id>[0-9]+)/(?P<template_id>[0-9]+)$', yatra_app_views.variations),
  url(r'^select_variation/(?P<category_id>[0-9]+)/(?P<template_id>[0-9]+)$', yatra_app_views.select_variation),
  url(r'^upload_images/(?P<category_id>[0-9]+)/(?P<template_id>[0-9]+)$', yatra_app_views.upload_images),
  url(r'^upload_videos/(?P<category_id>[0-9]+)/(?P<template_id>[0-9]+)$', yatra_app_views.upload_videos),
  url(r'^render/(?P<category_id>[0-9]+)/(?P<template_id>[0-9]+)$', yatra_app_views.render),
  url(r'^render_process/(?P<category_id>[0-9]+)/(?P<template_id>[0-9]+)$', render_app_views.render),
  url(r'^render_finished/(?P<video_session_id>[0-9]+)$', yatra_app_views.render_finished),
  url(r'^look_for_video/(?P<category_id>[0-9]+)/(?P<template_id>[0-9]+)$', yatra_app_views.look_for_video),
  url(r'^receive_video$', yatra_app_views.receive_video),
  url(r'^login$', accounts_views.login),
  url(r'^login_post$', accounts_views.login_post),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
