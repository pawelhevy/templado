from bootstrap3.forms import render_form
from django import template
from ..forms import SearchForm

register = template.Library()


@register.simple_tag()
def bootstrap_query_form(request):
    if request.GET.get('q'):
        form = SearchForm(request.GET)
    else:
        form = SearchForm()
    return render_form(form, layout='inline')


