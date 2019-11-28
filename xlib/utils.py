import re

from django.conf import settings


def extractor(text):
    pattern = re.compile(settings.REMIND_PATTERN, re.IGNORECASE)
    matched = pattern.findall(text)

    if matched:
        matched = matched[0]
        pattern = re.compile('\d+', re.IGNORECASE)
        duration = pattern.findall(matched)[0]
        unit = matched.split(duration)[1]
        return int(duration), unit

    return None
