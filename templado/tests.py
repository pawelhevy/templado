from django.test import TestCase
from .forms import FormFromPattern


class FormFromPatternTest(TestCase):
    def setUp(self):
        pattern = {
            "id": {
                "caption": "Numer faktury",
                "hint": "np. 21",
                "type": "text",
                "order": 1,
                "check": "^[0-9]+$"
            },
            "items": {
                "caption": "Towary",
                "order": 2,
                "type": [
                    {
                        "price": {
                            "caption": "Cena",
                            "hint": "np. 21.00",
                            "type": "text",
                            "order": 2,
                            "check": "^[0-9]+\\.[0-9][0-9]$"
                        },
                        "name": {
                            "caption": "Nazwa towaru",
                            "hint": "np. slodka bulka",
                            "type": "text",
                            "order": 1,
                            "check": ".+"
                        }
                    }
                ]
            }
        }
        self.form = FormFromPattern(pattern, True)

    # def test_form_has_nested

    def test_caption_is_missing_in_field(self):
        self.assertRaises(KeyError, FormFromPattern, {
            "id": {
                "hint": "np. 21",
                "type": "text",
                "order": 1,
                "check": "^[0-9]+$"
            }
        }, True)

    def test_hint_is_missing_in_field(self):
        self.assertRaises(KeyError, FormFromPattern, {
            "id": {
                "caption": "Numer faktury",
                "type": "text",
                "order": 1,
                "check": "^[0-9]+$"
            }
        }, True)

    def test_type_is_missing_in_field(self):
        self.assertRaises(KeyError, FormFromPattern, {
            "id": {
                "caption": "Numer faktury",
                "hint": "np. 21",
                "order": 1,
                "check": "^[0-9]+$"
            }
        }, True)

    def test_order_is_missing_in_field(self):
        self.assertRaises(KeyError, FormFromPattern, {
            "id": {
                "caption": "Numer faktury",
                "hint": "np. 21",
                "type": "text",
                "check": "^[0-9]+$"
            }
        }, True)

    def test_check_is_missing_in_field(self):
        self.assertRaises(KeyError, FormFromPattern, {
            "id": {
                "caption": "Numer faktury",
                "hint": "np. 21",
                "type": "text",
                "order": 1
            }
        }, True)

    def test_form_raises_error_without_pattern_and_tags(self):
        with self.assertRaises(TypeError):
            FormFromPattern()


