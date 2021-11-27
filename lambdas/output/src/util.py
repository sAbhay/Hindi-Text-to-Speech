from ipapy import UNICODE_TO_IPA as UNICODE_TO_IPA_CHAR
from constants import *
from enum import IntEnum


def is_long_vowel(c1: str, c2: str) -> bool:
    if "vowel" in UNICODE_TO_IPA_CHAR[c1].descriptors:
        if c2 == "ː" or "vowel" in UNICODE_TO_IPA_CHAR[c2].descriptors:
            return True
    return False


class Weight(IntEnum):
    LIGHT = 1
    HEAVY = 2
    EXTRA_HEAVY = 3


def define_syllable_weight(syllable: str) -> Weight:
    if len(syllable) < 2 or ("vowel" in UNICODE_TO_IPA_CHAR[syllable[-1]].descriptors and not is_long_vowel(syllable[-2], syllable[-1])):
        return Weight.LIGHT
    if len(syllable) >= 2:
        if is_long_vowel(syllable[-2], syllable[-1]) or \
                ("vowel" in UNICODE_TO_IPA_CHAR[syllable[-1]].descriptors and not is_long_vowel(syllable[-2], syllable[-1])
                and "consonant" in UNICODE_TO_IPA_CHAR[syllable[-2]].descriptors):
            return Weight.HEAVY
    return Weight.EXTRA_HEAVY


def is_vowel(charname: str) -> bool:
    return "VOWEL" in charname or UNICODE_NAMES[charname] in VOWEL_LETTERS


def is_consonant(charname: str) -> bool:
    return "LETTER" in charname and UNICODE_NAMES[charname] not in VOWEL_LETTERS
