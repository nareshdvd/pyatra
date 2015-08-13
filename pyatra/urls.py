from django.conf.urls import include, url, patterns
# from django.contrib import admin
from django.conf.urls.static import static
from pyatra import settings
from admins import urls as admins_urls
from accounts import urls as accounts_urls
from yatra import urls as yatra_urls

urlpatterns = patterns('',
    url(r'^admins/', include(admins_urls, namespace='admins')),
    url(r'^$', 'yatra.views.home'),
    url(r'^accounts/', include(accounts_urls, namespace="accounts")),
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^yatra/', include(yatra_urls, namespace="yatra")),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
