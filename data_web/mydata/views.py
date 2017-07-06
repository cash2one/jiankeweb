# -*- coding:utf-8 -*-

import logging

from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import auth

from .plots import SeriesCharts
from .models import Person
from .forms import LoginForm

logger = logging.getLogger('data')


def logout(request):
    logger.debug('\033[96m 用户{}已登出! \033[0m'.format(request.user.username))
    auth.logout(request)
    return HttpResponseRedirect(reverse('mydata:index'))

class LoginView(TemplateView):
    template_name = "mydata/login.html"

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        post = request.POST.copy()
        form = LoginForm(data=post)
        if form.is_valid():
            logger.debug('\033[96m post data: {} \033[0m'.format(form.cleaned_data))
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = auth.authenticate(username=username, password=password)
            #import pdb
            #pdb.set_trace()
            if user is not None and user.is_active:
                auth.login(request, user)
                referer = request.META['HTTP_REFERER']
                if 'next' in referer:
                    url_name = 'mydata:{}'.format(referer.split('/')[-1])
                else:
                    url_name = 'mydata:index'
                return HttpResponseRedirect(reverse(url_name))
            else:
                return render(request, self.template_name, {'form': form,'password_is_wrong':True})
        else:
            logger.error("\033[92m LoginView: form.errors:{} \033[0m".format(form.errors))
        return render(request, self.template_name, {'form': form})


class IndexView(TemplateView):
    template_name = "mydata/index.html"

    def get(self, request):
        if request.user.is_authenticated():
            line_plot = SeriesCharts().line_chart()
            bar_plot = SeriesCharts().bar_chart()
            pie_plot = SeriesCharts().pie_chart()
            items = Person.objects.values('id', 'name', 'age', 'test')
            return render(request, self.template_name, locals())
        else:
            logout(request)
            return HttpResponseRedirect(reverse('mydata:login'))


class TablesView(TemplateView):
    template_name = "mydata/tables.html"
    def get(self, request):
        if request.user.is_authenticated():
            return render(request, self.template_name, locals())
        else:
            logout(request)
            return HttpResponseRedirect(reverse('mydata:login'))


class TablesDynamicView(TemplateView):
    template_name = "mydata/tables_dynamic.html"
