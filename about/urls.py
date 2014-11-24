from django.conf.urls import patterns

from about.views import AboutView

urlpatterns = patterns(
    '',
    (r'^$', AboutView.as_view(), {'slug': 'index'}),
    (r'^/(?P<slug>.+)$', AboutView.as_view()),
)
