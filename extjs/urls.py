from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from rest_framework import routers

from extjs.demo.views import UserViewSet, GroupViewSet


from django.contrib import admin
admin.autodiscover()


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)


urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='homepage'),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
)
