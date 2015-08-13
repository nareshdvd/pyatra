from django.conf.urls import include, url
from accounts import views

urlpatterns = [
  url(r'^signin$', views.signin, name='signin'),
  url(r'^signin_post$', views.signin_post, name='signin_post'),
  url(r'^signout$', views.signout, name='signout'),
]