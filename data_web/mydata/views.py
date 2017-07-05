# -*- coding:utf-8 -*-

import logging

from django.shortcuts import render
from django.views.generic import TemplateView
from django_tables2 import RequestConfig
from .tables import PersonTable

from .plots import SeriesCharts
from .models import Person

logger = logging.getLogger('data')


class IndexView(TemplateView):
    template_name = "mydata/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['line_plot'] = SeriesCharts().line_chart()
        context['bar_plot'] = SeriesCharts().bar_chart()
        context['pie_plot'] = SeriesCharts().pie_chart()
        items = Person.objects.values('id', 'name', 'age', 'test')
        context['items']  = items
        return context


class TablesView(TemplateView):
    template_name = "mydata/tables.html"


class TablesDynamicView(TemplateView):
    template_name = "mydata/tables_dynamic.html"

class TempPlotView(TemplateView):
    template_name = "mydata/temp-plot.html"


def people(request):
    table = PersonTable(Person.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'mydata/people.html', {'table': table})


