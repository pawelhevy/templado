from django.core.urlresolvers import reverse
from django.test import TestCase

# Create your tests here.
from .forms import FormFromPattern


class FormFromPatternTest(TestCase):
    def test_form_is_created_from_pattern(self):
        url = reverse('')