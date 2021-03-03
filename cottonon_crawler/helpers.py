import re

from .utils import GENDER_MAP, Gender


def clean(lst_or_str):
    def sanitize(input_val):
        return re.sub(r'\s+', ' ', input_val.replace('\xa0', ' ')).strip()

    if not isinstance(lst_or_str, str) and getattr(lst_or_str, '__iter__', False):
        return [x for x in (sanitize(y) for y in lst_or_str if y is not None) if x]

    return sanitize(lst_or_str)


def detect_gender(str_or_lst):
    detected_genders = []
    if isinstance(str_or_lst, list):
        str_or_lst = ' '.join(str_or_lst)

    for key, gender in GENDER_MAP.items():
        if key in str_or_lst.lower():
            detected_genders.append(gender)

    for gender in Gender:
        if gender.value in detected_genders:
            return gender.value

    return Gender.ADULTS.value
