from django.core.exceptions import ValidationError
from datetime import date


def birth_validation(value):
    today = date.today()
    eighteen_years_ago = today.replace(year=today.year - 18)
    if not date(1990, 1, 1) <= value <= eighteen_years_ago:
        raise ValidationError("Date must be between %s and %s" % (date(1990, 1, 1), eighteen_years_ago))
