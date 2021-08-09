from ipapy import UNICODE_TO_IPA as UNICODE_TO_IPA_CHAR
from constants import *


def is_long_vowel(c1: str, c2: str) -> bool:
    if "vowel" in UNICODE_TO_IPA_CHAR[c1].descriptors:
        if c2 == "ː" or "vowel" in UNICODE_TO_IPA_CHAR[c2].descriptors:
            return True
    return False


def is_vowel(charname: str) -> bool:
    return "VOWEL" in charname or UNICODE_NAMES[charname] in VOWEL_LETTERS


def is_consonant(charname: str) -> bool:
    return "LETTER" in charname and UNICODE_NAMES[charname] not in VOWEL_LETTERS
