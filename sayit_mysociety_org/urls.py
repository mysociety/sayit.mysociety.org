import re
import sys

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import RedirectView
import django.views.static

from instances.views import InstanceUpdate
import login_token.views

from views import ShareWithCollaborators, AcceptInvite

urlpatterns = staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# If we're running test, then we need to serve static files even though DEBUG
# is false to prevent lots of 404s. So let's do what staticfiles_urlpatterns
# would do.
if 'test' in sys.argv:
    static_url = re.escape(settings.STATIC_URL.lstrip('/'))
    urlpatterns += [
        url(r'^%s(?P<path>.*)$' % static_url, django.views.static.serve, {
            'document_root': settings.STATIC_ROOT,
        }),
        url('^(?P<path>favicon\.ico)$', django.views.static.serve, {
            'document_root': settings.STATIC_ROOT,
        }),
    ]

if settings.DEBUG and settings.DEBUG_TOOLBAR:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

urlpatterns += [
    # For an instance domain, redirect to the instance home on login.
    url('^accounts/profile/', RedirectView.as_view(url='/', permanent=False)),
    url(r'^accounts/', include('allauth.urls')),

    url(r'^instance/edit$', InstanceUpdate.as_view(), name='instance-edit'),
    url(r'^instance/token$',
        login_token.views.login_tokens_for_user,
        name='tokens'),

    url(r'^instance/share$',
        ShareWithCollaborators.as_view(),
        name='share_instance'),
    url(r'^instance/invite/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$',
        AcceptInvite.as_view(),
        name='instance_accept_invite'),

    url(r'^about', include('about.urls')),
    url(r'^',
        include('speeches.urls', app_name='speeches', namespace='speeches')),
]
