from django.conf.urls import url

from about.views import AboutView

urlpatterns = [
    url(r'^$', AboutView.as_view(), {'slug': 'index'}),
    url(r'^/(?P<slug>.+)$', AboutView.as_view()),
]
