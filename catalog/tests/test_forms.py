import datetime

from django.test import TestCase

from catalog.forms import RenewBookForm


class RenewBookFormTest(TestCase):

    def test_renewal_date_field_label(self):
        form = RenewBookForm(data = {
            'renewal_date': datetime.date.today(),
        })
        self.assertEqual(
            form.fields['renewal_date'].label,
            "Renewal date"
        )

    def test_renewal_date_field_helptext(self):
        form = RenewBookForm(data = {
            'renewal_date': datetime.date.today(),
        })
        self.assertEqual(
            form.fields['renewal_date'].help_text,
            "Enter a date between now and 4 weeks (default 3)"
        )

    def test_renewal_date_validate_today(self):
        form = RenewBookForm(data = {
            'renewal_date': datetime.date.today(),
        })
        self.assertTrue(form.is_valid())

    def test_renewal_date_validate_max_allowed_date(self):
        form = RenewBookForm(data = {
            'renewal_date': datetime.date.today() + datetime.timedelta(weeks=4),
        })
        self.assertTrue(form.is_valid())

    def test_renewal_date_validate_future_date(self):
        date = datetime.date.today() + \
               datetime.timedelta(weeks=4) + \
               datetime.timedelta(days=1)
        form = RenewBookForm(data = {
            'renewal_date': date
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['renewal_date'],
            ["Invalid date - renewal more than 4 weeks ahead", ]
        )

    def test_renewal_date_validate_past_date(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form = RenewBookForm(data = {
            'renewal_date': date
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['renewal_date'],
            ["Invalid date - renewal in past", ]
        )