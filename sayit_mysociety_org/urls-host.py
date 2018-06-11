from django.conf import settings
from django.conf.urls import include, url

from tastypie.resources import ModelResource
from tastypie.api import Api

from instances.models import Instance
from instances.views import YourInstances

from views import InstanceCreate
import login_token.views

from django.contrib import admin


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

urlpatterns = [
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/tokens/?$', login_token.views.login_tokens_for_user, name='tokens'),
    url(r'^accounts/mobile-login', login_token.views.check_login_token),
    url(r'^accounts/profile/', YourInstances.as_view(), name='your_instances'),
    url(r'^accounts/', include('allauth.urls')),

    url(r'^instances/add', InstanceCreate.as_view(), name='create_instance'),

    url(r'^api/', include(v01_api.urls)),
    url(r'^about', include('about.urls')),

    url(r'^', include('instances.urls')),
]

if settings.DEBUG and settings.DEBUG_TOOLBAR:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
