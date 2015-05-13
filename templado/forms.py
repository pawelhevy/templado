from functools import wraps, partial
from django.core.validators import RegexValidator
from django.forms import Form, Field, CharField, TextInput, FileField
from collections import OrderedDict
from django.forms.formsets import formset_factory


class UploadStaticForm(Form):
    file = FileField()


class FormFromPattern(Form):
    def create_fields(self, pattern, *args, **kwargs):
        for key, value in pattern.iteritems():
            if key != 'STATIC_DIR':
                if isinstance(value['type'], unicode) or isinstance(value['type'], str):
                    self.fields[key] = CharField(required=True, label=value['caption'],
                                                 widget=TextInput(attrs={'placeholder': value['hint'],
                                                 }),
                                                 validators=[RegexValidator(value['check'], 'Wrong format')])
                elif isinstance(value['type'], list):  # formset
                    FormFromPatternFormSet = formset_factory(
                        wraps(FormFromPattern)(partial(FormFromPattern, pattern=value['type'][0], tags=False)),
                        extra=1, can_delete=True)
                    self.nested_formsets.append({'caption': value['caption'],
                                                 'name': key,
                                                 'formset': FormFromPatternFormSet(prefix=key, *args, **kwargs)})

    def __init__(self, pattern, tags, *args, **kwargs):
        super(FormFromPattern, self).__init__(*args, **kwargs)
        self.nested_formsets = []
        pattern = OrderedDict(sorted(pattern.items(), key=lambda i: i[1]['order']))
        self.create_fields(pattern, *args, **kwargs)
        if tags:
            self.fields['tags'] = CharField(required=False, label='Tags',
                                            widget=TextInput(attrs={'placeholder': 'Tags separated with comma',
                                            }), )

    def is_valid(self):
        form_is_valid = super(FormFromPattern, self).is_valid()
        for nested_formset in self.nested_formsets:
            if not nested_formset['formset'].is_valid():
                form_is_valid = False
        return form_is_valid

    def process(self):
        data = self.cleaned_data
        for nested_formset in self.nested_formsets:
            formset_data = [f.cleaned_data for f in nested_formset['formset'] if f.cleaned_data]
            data[nested_formset['name']] = formset_data
        return data


class SearchForm(Form):
    q = CharField(required=False, label='Search')