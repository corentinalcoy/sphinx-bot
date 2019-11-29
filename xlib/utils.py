import re

from django.conf import settings

from dateutil.parser import parse as date_parser
from django.utils.timezone import get_default_timezone



def extractor(text):
    pattern = re.compile(settings.REMIND_PATTERN, re.IGNORECASE)
    matched = pattern.findall(text)

    if matched:
        matched = matched[0]
        pattern = re.compile('\d+', re.IGNORECASE)
        duration = pattern.findall(matched)[0]
        unit = _format_unit(matched.split(duration)[1].strip())

        if 'year' in unit:
            duration *= 12
            unit = "months"

        return int(duration), unit

    return None


def _format_unit(unit):
    if not unit.endswith('s'):
        unit += 's'
    return unit

def parse_date(date_str):
    if not date_str:
        return None

    date = date_parser(date_str)

    if not date.tzinfo:
        date = date.replace(tzinfo=get_default_timezone())

    return date
