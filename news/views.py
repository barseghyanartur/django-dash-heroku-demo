from django.http import Http404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import gettext_lazy as _

from dash.base import get_layout
from dash.utils import get_or_create_dashboard_settings
from .models import NewsItem
from .constants import (
    MAX_NUM_POSTS_LISTING,
    PAGE_URL_PARAM,
    NUM_POSTS_URL_PARAM,
)
from .defaults import DEFAULT_MAX_NEWS_ITEMS

__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = 'Copyright (c) 2013 Artur Barseghyan'
__license__ = 'GPL-2.0-only OR LGPL-2.1-or-later'
__all__ = ('browse', 'detail')


@csrf_exempt
@login_required
def browse(request,
           template_name='news/browse.html',
           template_name_ajax='news/browse_ajax.html'):
    """
    In the template, we show all available NewsItems for current language.

    :param django.http.HttpRequest request:
    :param string template_name:
    :return django.http.HttpResponse:
    """
    # Getting dashboard settings for the user. Then get users' layout.
    dashboard_settings = get_or_create_dashboard_settings(request.user)
    layout = get_layout(
        layout_uid=dashboard_settings.layout_uid, as_instance=True
    )

    results_kwargs = {}

    queryset = NewsItem._default_manager.filter(**results_kwargs) \
                       .order_by('-date_published')

    page = request.GET.get(PAGE_URL_PARAM, 1)
    #import ipdb; ipdb.set_trace()
    num_posts = request.GET.get(NUM_POSTS_URL_PARAM, DEFAULT_MAX_NEWS_ITEMS)

    try:
        num_posts = int(num_posts)
    except Exception as e:
        num_posts = DEFAULT_MAX_NEWS_ITEMS

    if num_posts < 1 or num_posts > MAX_NUM_POSTS_LISTING:
        num_posts = DEFAULT_MAX_NEWS_ITEMS

    paginator = Paginator(queryset, num_posts, allow_empty_first_page=False)

    try:
        page_number = int(page)
    except ValueError as e:
        if 'last' == page:
            page_number = paginator.num_pages
        else:
            raise Http404(_("Invalid page!"))

    try:
        page_obj = paginator.page(page_number)
    except InvalidPage as e:
        raise Http404(_("Invalid page!"))

    context = {
        'layout': layout,

        'PAGE_URL_PARAM': PAGE_URL_PARAM,
        'NUM_POSTS_URL_PARAM': NUM_POSTS_URL_PARAM,

        # Pagination specific
        'paginator': paginator,
        'page_obj': page_obj,
        'results_per_page': paginator.per_page,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
        'page': page_obj.number,
        'next': page_obj.next_page_number() if page_obj.has_next() and page_obj.next_page_number() is not None else '',
        'previous': page_obj.previous_page_number() if page_obj.has_previous() and page_obj.previous_page_number() is not None else '',
        'first_on_page': page_obj.start_index(),
        'last_on_page': page_obj.end_index(),
        'pages': paginator.num_pages,
        'hits': paginator.count,
        'page_range': paginator.page_range,
        'items': page_obj.object_list,
        'request_path': request.path
    }

    if request.is_ajax():
        template_name = template_name_ajax

    return render(request, template_name, context)


def detail(request,
           slug,
           template_name='news/detail.html',
           template_name_ajax='news/detail_ajax.html'):
    """
    News item detail. In the template, we show the title and the body of the
    News item and links to all its' all available translations.

    :param django.http.HttpRequest request:
    :param string slug: Foo item slug.
    :param string template_name:
    :return django.http.HttpResponse:
    """
    layout = get_layout(as_instance=True)

    results_kwargs = {'slug': slug}

    try:
        queryset = NewsItem._default_manager.filter(**results_kwargs)

        item = queryset.get(**results_kwargs)
    except Exception as e:
        raise Http404

    context = {
        'layout': layout,
        'item': item
    }

    if request.is_ajax():
        template_name = template_name_ajax

    return render(request, template_name, context)
