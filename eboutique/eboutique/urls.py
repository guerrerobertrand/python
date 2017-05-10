"""eboutique URL Configuration

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
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

# urlpatterns = [
#     url(r'^admin/', admin.site.urls),
# ]
# from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

# urlpatterns = patterns('',
#     # Examples:
#     # url(r'^$', 'eboutique.views.home', name='home'),
#     # url(r'^blog/', include('blog.urls')),
#
#     url(r'^admin/', include(admin.site.urls)),
#     url(r'^$', 'backoffice.views.home'),
# )

from django.conf.urls import patterns, include, url
from rest_framework import routers
from backoffice.views import *
# from erp.views import *
from django.contrib.auth.decorators import login_required

# urlpatterns = patterns('',
urlpatterns = patterns('',
    url(r'^admin/', admin.site.urls),
    url(r'^$', LoginView.as_view()),
    url(r'^logout/$', LogoutView.as_view()),
    url(r'^backoffice/$', login_required(TemplateView.as_view(template_name='backoffice/index.html'))),
)

#update urlpatterns to be a list of django.conf.urls.url() instances instead.
  # url(r'^backoffice/$', login_required(TemplateView.as_view(template_name='backoffice/index.html'))),

urlpatterns += patterns('', url(r'^medias/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),)
