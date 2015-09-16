from django.conf.urls import include, url
from renderapi import views
urlpatterns = [
    url(r'^render', views.render, name='render'),
    url(r'^restart_render', views.restart_render, name='restart_render'),
    url(r'^delete_job', views.delete_job, name='delete_job'),
    url(r'^send_finish_signal', views.send_finish_signal, name='send_finish_signal'),
]