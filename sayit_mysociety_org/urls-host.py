from django.conf import settings
from django.conf.urls import patterns, include, url

from tastypie.resources import ModelResource
from tastypie.api import Api

from instances.models import Instance
from instances.views import YourInstances

from views import InstanceCreate

# Admin section
from django.contrib import admin
admin.autodiscover()


class InstanceResource(ModelResource):
    class Meta:
        queryset = Instance.objects.all()
        allowed_methods = ['get']
        excludes = ['id']
        include_resource_uri = False
        include_absolute_url = True
        detail_uri_name = 'label'
        filtering = {'label': ['exact']}

v01_api = Api(api_name='v0.1')
v01_api.register(InstanceResource())

urlpatterns = patterns(
    '',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    url(r'^accounts/tokens/?$', 'login_token.views.login_tokens_for_user', name='tokens'),
    (r'^accounts/mobile-login', 'login_token.views.check_login_token'),
    url(r'^accounts/profile/', YourInstances.as_view(), name='your_instances'),
    (r'^accounts/', include('allauth.urls')),

    url(r'^instances/add', InstanceCreate.as_view(), name='create_instance'),

    (r'^api/', include(v01_api.urls)),
    (r'^about', include('about.urls')),

    (r'^', include('instances.urls')),
)

if settings.DEBUG and settings.DEBUG_TOOLBAR:
    import debug_toolbar
    urlpatterns += patterns(
        '',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
