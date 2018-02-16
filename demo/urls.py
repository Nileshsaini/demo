from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    # Examples:
    url(r'^$', 'demo.views.home', name='home'),
    url(r'^graph/', 'demo.views.graph', name='graph'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
]
