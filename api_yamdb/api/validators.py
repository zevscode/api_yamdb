import datetime as dt

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


def validate_year(value):
    if value < 1900 or value > dt.datetime.now().year:
        raise ValidationError(
            _('%(value)s неверно указан год !'),
            params={'value': value},
        )
