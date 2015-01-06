from django.urls import re_path as url

from .views import browse, detail

urlpatterns = [
    # Listing URL
    url(r'^$', view=browse, name='news.browse'),

    # Detail URL
    url(r'^(?P<slug>(?!overview\-)[\w\-\_\.\,]+)/$',
        view=detail,
        name='news.detail'),
]
