from django.conf.urls import include, url
from yatra import views

urlpatterns = [
  url(r'^$', views.home, name='home'),
  url(r'^categories$', views.categories, name="categories"),
]