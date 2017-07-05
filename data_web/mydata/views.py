# -*- coding:utf-8 -*-

import logging

from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django_tables2 import RequestConfig
from django.contrib.auth import authenticate, login

from .tables import PersonTable
from .plots import SeriesCharts
from .models import Person
from .forms import LoginForm

logger = logging.getLogger('data')


class LoginView(TemplateView):
    template_name = "mydata/login.html"

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        post = request.POST.copy()
        form = LoginForm(data=post)
        if form.is_valid():
            logger.debug('\033[92m post data: {} \033[0m'.format(form.clean()))
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('mydata:index'))
            else:
                return render(request, self.template_name, {'form': form,'password_is_wrong':True})
        else:
            logger.debug("LoginView: form.errors:{}".format(form.errors))
        return render(request, self.template_name, {'form': form})


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


