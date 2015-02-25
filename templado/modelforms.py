from django.forms.models import ModelForm
from .models import ReportTemplate


class ReportTemplateForm(ModelForm):
    class Meta:
        model = ReportTemplate
