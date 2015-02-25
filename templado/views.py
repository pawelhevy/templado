from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from django.views.generic.list import ListView
from models import Report, ReportTemplate
from .modelforms import ReportTemplateForm


class ReportsListView(ListView):
    model = Report


class TemplatesListView(ListView):
    model = ReportTemplate


class BaseReportFormView(View):
    template_name = None

    def get_form(self, data=None, *args, **kwargs):
        raise NotImplementedError

    def form_is_valid(self, data=None, *args, **kwargs):
        raise NotImplementedError

    def get(self, request, *args, **kwargs):
        form = self.get_form(*args, **kwargs)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.get_form(request.POST, *args, **kwargs)
        if form.is_valid():
            self.form_is_valid(form.process(), *args, **kwargs)
            return redirect('report-list')
        return render(request, self.template_name, {'form': form})


class ReportFormView(BaseReportFormView):
    template_name = 'templado/report_form.html'

    def get_template(self, **kwargs):
        return get_object_or_404(ReportTemplate, pk=kwargs['template'])

    def get_form(self, data=None, *args, **kwargs):
        return self.get_template(**kwargs).get_form(data)

    def form_is_valid(self, data=None, *args, **kwargs):
        Report.objects.create_report(self.get_template(**kwargs), data, data.get('tags'))


class EditReportFormView(BaseReportFormView):
    template_name = 'templado/report_form.html'

    def get_report(self, *args, **kwargs):
        return get_object_or_404(Report, pk=kwargs['report'])

    def get_form(self, data=None, *args, **kwargs):
        return self.get_report(**kwargs).get_form_with_content(data)

    def form_is_valid(self, data=None, *args, **kwargs):
        Report.objects.recreate_report(self.get_report(**kwargs), data, data.get('tags'))


class DownloadReport(View):
    def get(self, request, *args, **kwargs):
        report = get_object_or_404(Report, pk=kwargs['report'])
        filename = report.file.name.split('/')[-1]
        response = HttpResponse(report.file, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response


class TemplateFormView(View):
    template_name = 'templado/reporttemplate_form.html'

    def get_template(self, **kwargs):
        return get_object_or_404(ReportTemplate, pk=kwargs.get('template'))

    def get(self, request, *args, **kwargs):
        if kwargs.get('template'):
            form = ReportTemplateForm(instance=self.get_template(**kwargs))
        else:
            form = ReportTemplateForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        if kwargs.get('template'):
            form = ReportTemplateForm(request.POST, request.FILES, instance=self.get_template(**kwargs))
        else:
            form = ReportTemplateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('template-list')
        return render(request, self.template_name, {'form': form})


import re
from django.db.models import Q


def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:

        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.
    '''
    query = None  # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None  # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query


class SearchView(View):
    template_name = 'templado/report_list.html'

    def get(self, request, *args, **kwargs):
        query_string = ''
        found_entries = None
        if 'q' in request.GET and request.GET['q'].strip():
            query_string = request.GET['q']
            entry_query = get_query(query_string, ['name', 'tags', 'auto_tags'])
            found_entries = Report.objects.filter(entry_query)
            return render(request, self.template_name, {'object_list': found_entries,
                                                        'q': query_string, })
        raise PermissionDenied


class HelpView(View):
    template_name='templado/help_site.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})





