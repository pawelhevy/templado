from io import BytesIO
import json
from django.core.files.base import ContentFile
from django.db import models
from django.template import Template, Context
from django.conf import settings
from django.utils import timezone
from weasyprint import HTML
from .forms import FormFromPattern


class ReportTemplate(models.Model):
    title = models.CharField(unique=True, max_length=64, verbose_name='Title of template')
    template = models.FileField(verbose_name='HTML template file', upload_to='media/report-templates')
    pattern = models.FileField(verbose_name='JSON pattern file', upload_to='media/report-templates')
    tags = models.CharField(max_length=256, verbose_name='Tags')
    title_pattern = models.CharField(max_length=128, verbose_name='Pattern for title')
    tags_pattern = models.CharField(max_length=128, verbose_name='Pattern for tags')

    def __unicode__(self):
        return self.title

    def pattern_dict(self):
        ''' reads json file and returns data structure from it
        '''
        text = self.pattern.read()
        return json.loads(text)

    def get_form(self, *args, **kwargs):
        ''' returns form object based on json pattern
        '''
        return FormFromPattern(self.pattern_dict(), True, *args, **kwargs)


class ReportManager(models.Manager):
    def as_obj(self, report):
        if isinstance(report, str):
            report = self.get(pk=report)
        return report

    def create_report(self, template, data, tags=''):
        ''' creates new report and generates pdf based on data from new report
        '''
        data.update({'STATIC_DIR': settings.REPORT_STATIC_DIR})
        if isinstance(template, int):
            template = str(template)
        if isinstance(template, str):
            template = Report.objects.get(pk=template)
        report = self.model(template=template,
                            name=Template(template.title_pattern).render(Context(data)),
                            content=json.dumps(data),
                            auto_tags=Template(template.tags_pattern).render(Context(data)),
                            tags=' '.join(tags.split()),
                            )
        report.started = timezone.now()
        report.generate_pdf()
        report.finished = timezone.now()
        report.save()
        return report

    def recreate_report(self, report, data={}, tags=''):
        ''' changes attributes of report given new data and generates data
        '''
        data.update({'STATIC_DIR': settings.REPORT_STATIC_DIR})
        report = self.as_obj(report)
        if data:
            data.update(data)
            report.content = json.dumps(data)
            report.name = Template(report.template.title_pattern).render(Context(data))
            report.auto_tags = Template(report.template.tags_pattern).render(Context(data))
            report.generate_pdf()
        if tags:
            self.tag(report, tags)
        report.save()
        return report

    def tag(self, report, tags):
        ''' adds new tags for given report
        '''
        report = self.as_obj(report)
        all_tags = ' '.join(report.tags.split() + tags.split())
        report.tags = all_tags
        report.save()
        return report

    def all_reports(self, tags=''):
        if tags:
            from django.db.models import Q
            return self.filter(Q(tags__icontains=tags) | Q(auto_tags__icontains=tags))
        return self.all()


class Report(models.Model):
    template = models.ForeignKey(ReportTemplate, verbose_name='Template for report')
    name = models.CharField(null=True, blank=True, max_length=128, verbose_name='Title of report')
    content = models.TextField(null=True, blank=True, verbose_name='JSON content for generating PDF')
    file = models.FileField(null=True, blank=True, verbose_name='Generated PDF file', upload_to='media/report-files')
    started = models.DateTimeField(default=None, null=True, blank=True, verbose_name='Start date of generating file')
    finished = models.DateTimeField(default=None, null=True, blank=True, verbose_name='Finish date of generating file')
    tags = models.CharField(null=True, blank=True, max_length=128, verbose_name='Tags for report')
    auto_tags = models.CharField(null=True, blank=True, max_length=128, verbose_name='Generated tags')
    objects = ReportManager()

    def __unicode__(self):
        return self.name

    @property
    def all_tags(self):
        return ' '.join(self.tags.split() + self.auto_tags.split())

    def form_content(self):
        ''' converts its content to format that is accepted by formsets
        '''
        content = json.loads(self.content)
        flat_content = {}
        for k, v in content.iteritems():
            if isinstance(v, list):
                flat_content.update({
                    k + '-TOTAL_FORMS': len(v),
                    k + '-INITIAL_FORMS': u'0',
                    k + '-MAX_NUM_FORMS': u'',
                })
                for i, element in enumerate(v):
                    for u, w in element.iteritems():
                        flat_content.update({k + '-' + str(i) + '-' + u: w})
            else:
                flat_content.update({k: v})
        return flat_content

    def get_form_with_content(self, data=None, *args, **kwargs):
        ''' generates form from template and fills it with its formatted content
        '''
        return self.template.get_form(data) if data \
            else self.template.get_form(self.form_content())

    def generate_pdf(self):
        ''' renders html from file with given context and creates pdf file from it
        '''
        html_string = Template(self.template.template.read()).render(Context(json.loads(self.content)))
        html = HTML(string=html_string, base_url='')
        filename = self.name.replace('/', '.') + '.pdf'
        buffer = BytesIO()
        html.write_pdf(target=buffer)
        pdf = buffer.getvalue()
        buffer.close()
        self.file.save(filename, ContentFile(pdf))


