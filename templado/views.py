import os
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from django.views.generic.list import ListView
import errno
from models import Report, ReportTemplate
from .modelforms import ReportTemplateForm
from templado.forms import UploadStaticForm
from templado.functions import save_static_file, get_uploaded_static_files


class ReportsListView(ListView):
    """
        Displays list of reports uses generic class based list view
        template_name = report_list.html
    """
    model = Report


class TemplatesListView(ListView):
    """
        Displays list of report templates uses generic class based list view
        template_name = reporttemplate_list.html
    """
    model = ReportTemplate


class BaseFormView(View):
    """
        Base form view interface is used in ReportFormView in EditReportFormView
    """
    template_name = 'templado/report_form.html'
    redirect_url = 'templado:report-list'

    def get_form(self, data=None, *args, **kwargs):
        """Takes form to display with proper data"""
        raise NotImplementedError

    def form_is_valid(self, data=None, *args, **kwargs):
        """actions after form validation"""
        raise NotImplementedError

    def get(self, request, *args, **kwargs):
        """displays proper form"""
        form = self.get_form(*args, **kwargs)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        """takes context from request and validates form"""
        form = self.get_form(request.POST, *args, **kwargs)
        if form.is_valid():
            self.form_is_valid(form.process(), *args, **kwargs)
            return redirect(self.redirect_url)
        return render(request, self.template_name, {'form': form})


class UploadStaticView(View):
    """
        View
    """
    template_name = 'templado/upload_static.html'
    redirect_url = 'templado:upload-static'

    def render(self, request, form):
        uploaded_files = get_uploaded_static_files()
        return render(request, self.template_name, {'form': form, 'files': uploaded_files})

    def get(self, request, *args, **kwargs):
        form = UploadStaticForm()
        return self.render(request, form)

    def post(self, request, *args, **kwargs):
        form = UploadStaticForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['file']
            save_static_file(f)
            return redirect(self.redirect_url)
        return self.render(request, form)


class ReportFormView(BaseFormView):
    """
        Inherits methods get and post from BaseReportFormView
    """

    def get_template(self, **kwargs):
        return get_object_or_404(ReportTemplate, pk=kwargs['template'])

    def get_form(self, data=None, *args, **kwargs):
        """for given template generates report form"""
        return self.get_template(**kwargs).get_form(data)

    def form_is_valid(self, data=None, *args, **kwargs):
        """when form is valid, creates report from template with given data"""
        Report.objects.create_report(self.get_template(**kwargs), data, data.get('tags'))


class EditReportFormView(BaseFormView):
    """
        Inherits methods get and post from BaseReportView
    """

    def get_report(self, *args, **kwargs):
        return get_object_or_404(Report, pk=kwargs['report'])

    def get_form(self, data=None, *args, **kwargs):
        """for given report generates report form and fills it with its data"""
        return self.get_report(**kwargs).get_form_with_content(data)

    def form_is_valid(self, data=None, *args, **kwargs):
        """recreates report with new data"""
        Report.objects.recreate_report(self.get_report(**kwargs), data, data.get('tags'))


class DownloadReport(View):

    def get(self, request, *args, **kwargs):
        """returns pdf file with report"""
        report = get_object_or_404(Report, pk=kwargs['report'])
        filename = report.file.name.split('/')[-1]
        response = HttpResponse(report.file, content_type='application/pdf; charset=utf-8')
        response['Content-Disposition'] = 'inline; filename=%s' % filename
        return response


class TemplateFormView(View):
    """
        Form view for creating template objects
    """
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
            return redirect('templado:template-list')
        return render(request, self.template_name, {'form': form})


class HelpView(View):
    """
        Static help page
    """
    template_name='templado/help_site.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


import re
from django.db.models import Q


def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    """ Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:

        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

    """
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


def get_query(query_string, search_fields):
    """ Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.
    """
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
    """
        Simple search view for reports
    """
    template_name = 'templado/report_list.html'

    def get(self, request, *args, **kwargs):
        query_string = ''
        if 'q' in request.GET and request.GET['q'].strip():
            query_string = request.GET['q']
            entry_query = get_query(query_string, ['name', 'tags', 'auto_tags'])
            found_entries = Report.objects.filter(entry_query)
        else:
            found_entries = Report.objects.all()
        return render(request, self.template_name, {'object_list': found_entries,
                                                    'q': query_string, })