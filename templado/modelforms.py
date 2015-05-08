import json
from django.forms.models import ModelForm
from .models import ReportTemplate
from templado.forms import FormFromPattern


class ReportTemplateForm(ModelForm):

    class Meta:
        model = ReportTemplate
        fields = "__all__" 

    def clean_pattern(self):
        data = self.cleaned_data.get('pattern')
        try:
            pattern = json.loads(data.read())
            FormFromPattern(pattern, True)
        except (KeyError, ValueError):
            msg = 'Format of fields in json file is wrong'
            self.add_error('pattern', msg)

        return data