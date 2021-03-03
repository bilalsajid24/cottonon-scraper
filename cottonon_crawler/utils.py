from enum import Enum


class Gender(Enum):
    """
    This is the default order for which the genders will be detected
    """

    GIRLS = 'girls'
    BOYS = 'boys'
    KIDS = 'unisex-kids'
    WOMEN = 'women'
    MEN = 'men'
    ADULTS = 'unisex-adults'


GENDER_MAP = {
    'men': Gender.MEN.value,
    'man': Gender.MEN.value,
    'mens': Gender.MEN.value,

    'women': Gender.WOMEN.value,
    'womens': Gender.WOMEN.value,
    'woman': Gender.WOMEN.value,

    'boy': Gender.BOYS.value,
    'boys': Gender.BOYS.value,

    'girl': Gender.GIRLS.value,
    'girls': Gender.GIRLS.value,

    'kids': Gender.KIDS.value,
    'kid': Gender.KIDS.value,
    'baby': Gender.KIDS.value,
    'babies': Gender.KIDS.value,
}
