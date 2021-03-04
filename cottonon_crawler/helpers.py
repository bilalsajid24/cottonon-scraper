import re

from .utils import GENDER_MAP, Gender


def remove_spaces_and_strip(value):
    return re.sub(r'\s+', ' ', value.replace('\xa0', ' ')).strip()


def clean(lst_or_str):
    if isinstance(lst_or_str, list):
        return [x for x in (remove_spaces_and_strip(y) for y in lst_or_str if y is not None) if x]

    return remove_spaces_and_strip(lst_or_str)


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

    # Return default gender value
    return Gender.ADULTS.value
