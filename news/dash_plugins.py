from django.utils.translation import gettext_lazy as _

from dash.base import BaseDashboardPlugin
from dash.factory import plugin_factory, plugin_widget_factory

from .models import NewsItem
from .forms import NewsForm
from .dash_widgets import BaseNewsWidget

__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = 'Copyright (c) 2013 Artur Barseghyan'
__license__ = 'GPL-2.0-only OR LGPL-2.1-or-later'
__all__ = ('BaseNewsPlugin',)

# *****************************************************************************
# ****************************** Base News plugin *****************************
# *****************************************************************************


class BaseNewsPlugin(BaseDashboardPlugin):
    """
    Base news plugin.
    """
    name = _("News")
    form = NewsForm
    group = _("News")

    def post_processor(self):
        """
        Getting news items for the current active language.
        """
        results_kwargs = {}

        self.data.news_items = NewsItem._default_manager.filter(
            **results_kwargs
        ).order_by('-date_published')[:self.data.max_items]

# *****************************************************************************
# ********** Generating and registering the plugins using factory *************
# *****************************************************************************

sizes = (
    (2, 5),
    (4, 5)
)

plugin_factory(BaseNewsPlugin, 'news', sizes)

# ****************************************************************************
# ****************** Registering widgets for News plugin *********************
# ****************************************************************************

main_sizes = (
    (2, 5),
    (4, 5),
)
plugin_widget_factory(BaseNewsWidget, 'android', 'main', 'news', main_sizes)
