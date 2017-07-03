# -*- coding:utf-8 -*-

import logging

from django.shortcuts import render
from django.views.generic import TemplateView

from .plots import SeriesCharts

logger = logging.getLogger('data')


class IndexView(TemplateView):
    template_name = "mydata/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['plot'] = SeriesCharts().line_charts()
        return context
