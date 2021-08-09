import unicodedata
from constants import *
import logging
from ipapy import UNICODE_TO_IPA as UNICODE_TO_IPA_CHAR
from ipapy.ipachar import IPAConsonant, IPAVowel
import util


logging.basicConfig(level=logging.DEBUG)


def transcribe_to_ipa(text: str) -> str:
    words = text.split(" ")
    ipa_words = []
    for i, word in enumerate(words):
        if len(word) == 0:
            logging.debug(f"empty word at position {i}")
            continue

        ipa_word = ""
        names = [unicodedata.name(c) for c in word]
        logging.debug(f"Names: {names}")

        # handle edge cases
        chars = transcribe_viramas(names)
        logging.debug(f"Viramas: {chars}")
        chars = transcribe_nuktas(chars)
        logging.debug(f"Nuktas: {chars}")
        chars = add_schwas(chars)
        logging.debug(f"Add Schwas: {chars}")
        chars = syncopate_schwas(chars)
        logging.debug(f"Delete Schwas: {chars}")
        chars = transcribe_visargas(chars)
        logging.debug(f"Visargas: {chars}")
        chars = transcribe_chandrabindus_and_anuswaras(chars)
        logging.debug(f"Chandrabindus: {chars}")

        for i, c in enumerate(chars):
            if c in UNICODE_TO_IPA:
                ipa_word += UNICODE_TO_IPA[c]
            else:
                # this should never happen
                if "DEVANAGARI" in c:
                    raise Exception(f"unhandled character at position {i}: {c}")

                # already converted in earlier steps
                ipa_word += c

        ipa_word = assimilate_nasal_place(ipa_word)
        logging.debug(f"Nasal place assimilation: {ipa_word}")
        ipa_word = add_syllable_boundaries(ipa_word)
        logging.debug(f"Syllable boundaries: {ipa_word}")

        ipa_words.append(ipa_word)

    ipa = " ".join(ipa_words)
    return ipa


def transcribe_viramas(charnames: list) -> list:
    if len(charnames) < 3:
        return charnames

    cleaned = [charnames[0]]
    i = 1
    while i < len(charnames)-1:
        if charnames[i-1] == 'DEVANAGARI LETTER JA' \
                and charnames[i] == 'DEVANAGARI SIGN VIRAMA' \
                and charnames[i+1] == 'DEVANAGARI LETTER NYA':
            cleaned[-1] = 'gj'
            i += 2
            continue

        elif charnames[i] == 'DEVANAGARI SIGN VIRAMA':
            # in case of existing consonant cluster
            if "DEVANAGARI" not in cleaned[-1]:
                cleaned[-1] = cleaned[-1] + UNICODE_TO_IPA[charnames[i + 1]]
            else:
                cleaned[-1] = UNICODE_TO_IPA[charnames[i-1]] + UNICODE_TO_IPA[charnames[i+1]]
            i += 2
            continue

        cleaned.append(charnames[i])
        i += 1
    if i != len(charnames):
        cleaned += charnames[-1:]
    return cleaned


def transcribe_visargas(charnames: list) -> list:
    if len(charnames) == 0:
        return charnames

    cleaned = [charnames[0]]
    i = 1
    while i < len(charnames):
        if charnames[i] == 'DEVANAGARI SIGN VISARGA':
            if "VOWEL" in charnames[i-1]:
                realization = UNICODE_TO_IPA[charnames[i-1]] + 'h'
                if i == len(charnames)-1:
                    realization += UNICODE_TO_IPA[charnames[i-1]]
                    if realization[-1] == "ː":
                        realization = realization[:-1]
                cleaned[-1] = realization
            else:
                realization = 'əhə'
                if charnames[i-1] == 'ə':
                    realization = 'hə'
                cleaned.append(realization)
            i += 1
            continue
        cleaned.append(charnames[i])
        i += 1
    return cleaned


def transcribe_nuktas(charnames: list) -> list:
    cleaned = []
    i = 0
    while i < len(charnames)-1:
        cleaned.append(charnames[i])
        if charnames[i+1] == 'DEVANAGARI SIGN NUKTA':
            if charnames[i] == 'DEVANAGARI LETTER KHA':
                cleaned[-1] = 'x'
            elif charnames[i] == 'DEVANAGARI LETTER JHA':
                cleaned[-1] = 'ʒ'
            i += 2
            continue
        i += 1
    if charnames[-1] != 'DEVANAGARI SIGN NUKTA':
        cleaned += charnames[-1:]
    return cleaned


def add_schwas(charnames: list) -> list:
    cleaned = []
    i = 0
    while i < len(charnames):
        cleaned.append(charnames[i])
        if util.is_consonant(charnames[i]) \
                or (charnames[i] not in UNICODE_TO_IPA and "DEVANAGARI" not in charnames[i]):
            if i == len(charnames)-1:
                cleaned.append('ə')
            elif "VIRAMA" in charnames[i+1]:
                i += 2
                continue
            elif "VOWEL" not in charnames[i+1] or charnames[i+1] not in UNICODE_TO_IPA:
                cleaned.append('ə')
        i += 1
    return cleaned


def syncopate_schwas(charnames: list) -> list:
    if len(charnames) <= 2:
        return charnames

    # delete final schwa unless final consonant cluster produced
    if charnames[-1] == 'ə' and not (len(charnames[-2]) > 1 and 'DEVANAGARI' not in charnames[-2]):
        charnames = charnames[:-1]

    if len(charnames) < 5:
        return charnames

    cleaned = charnames[:2]
    i = 2
    while i < len(charnames)-2:
        if charnames[i] == 'ə':
            if ("VOWEL" in charnames[i-2] or charnames[i-2] == 'ə') \
                    and (("LETTER" in charnames[i-1] and "VOWEL" not in charnames[i-1]) or ('DEVANAGARI' not in charnames[-2] and len(charnames[-2]) > 1)) \
                    and (("LETTER" in charnames[i+1] and "VOWEL" not in charnames[i+1]) or ('DEVANAGARI' not in charnames[-2] and len(charnames[-2]) > 1)) \
                    and ("VOWEL" in charnames[i+2] or charnames[i-2] == 'ə'):
                i += 1
                continue
        cleaned.append(charnames[i])
        i += 1
    cleaned += charnames[-2:]
    return cleaned

def transcribe_chandrabindus_and_anuswaras(chars: list) -> list:
    if len(chars) == 0:
        return chars

    cleaned = [chars[0]]
    i = 1
    while i < len(chars):
        if chars[i] == 'DEVANAGARI SIGN CANDRABINDU' or chars[i] == 'DEVANAGARI SIGN ANUSVARA':
            if chars[i-1] == 'ə':
                nasalized = "̃" + 'ə'
            elif util.is_vowel(chars[i-1]):
                nasalized = '̃' + UNICODE_TO_IPA[chars[i-1]]
            else:
                raise ValueError(f"invalid input, non-vowel {chars[i-1]} precedes chandrabindu or bindu")

            if chars[i] == 'DEVANAGARI SIGN ANUSVARA':
                if i == len(chars)-1:
                    if chars[i-1] == 'ə':
                        nasalized += 'm'
                elif util.is_consonant(chars[i+1]):
                    nasalized += 'n'

            del cleaned[-1]
            cleaned.append(nasalized)
            i += 1
            continue
        cleaned.append(chars[i])
        i += 1
    return cleaned


def assimilate_nasal_place(word: str) -> str:
    cleaned = ""
    for i, c in enumerate(word):
        to_add = c
        if c == 'n':
            if i < len(word)-1:
                next = UNICODE_TO_IPA_CHAR[word[i+1]]
                if type(next) == IPAConsonant and word[i+1] != 'n':
                    if 'bilabial' in next.descriptors:
                        to_add = 'm'
                    if 'labio-dental' in next.descriptors:
                        to_add = 'm'
                    if 'alveolar' in next.descriptors:
                        to_add = 'n'
                    if 'retroflex' in next.descriptors:
                        to_add = 'ɳ'
                    if 'alveo-palatal' in next.descriptors or 'palatal' in next.descriptors:
                        to_add = 'ɲ'
                    if 'velar' in next.descriptors:
                        to_add = 'ŋ'
                    if 'uvular' in next.descriptors:
                        to_add = 'ɴ'
        cleaned += to_add
    return cleaned


def add_syllable_boundaries(word: str) -> str:
    syllables = []
    contains_vowel = False
    syllable = ""
    for i, c in enumerate(word):
        current = UNICODE_TO_IPA_CHAR[c]
        if i == len(word) - 1:
            syllable += c
            syllables.append(syllable)
            break
        if "consonant" in current.descriptors:
            next_char = None
            skip = 0
            while next_char is None or (
                    "vowel" not in next_char.descriptors and "consonant" not in next_char.descriptors):
                if i+1+skip == len(word):
                    break
                next_char = UNICODE_TO_IPA_CHAR[word[i+1+skip]]
                skip += 1
            if contains_vowel:
                if "vowel" in next_char.descriptors:
                    syllables.append(syllable)
                    syllable = ""
                    contains_vowel = False
                elif "consonant" in next_char.descriptors:
                    if syllable == "" or "consonant" in UNICODE_TO_IPA_CHAR[syllable[-1]].descriptors:
                        syllables.append(syllable)
                        syllable = ""
                        contains_vowel = False
            syllable += c
        elif "vowel" in current.descriptors:
            syllable += c
            contains_vowel = True
        else:
            syllable += c
    return '.'.join(syllables)


def add_suprasegmental_stress(word: str) -> str:
    syllables = word[:-1].split('.')
    weights = []
    for syllable in syllables:
        weights.append(util.define_syllable_weight(syllable))

    if all([weight == util.Weight.LIGHT for weight in weights]):
        stress_index = len(syllables)-2
    else:
        heaviest_weight = util.Weight.HEAVY
        heaviest_indices = []
        for i, weight in enumerate(weights):
            if weight == heaviest_weight:
                heaviest_indices.append(i)
            if weight > heaviest_weight:
                heaviest_weight = weight
                heaviest_indices = [i]
        stress_index = heaviest_indices[-1]

    syllables[stress_index] = 'ˈ' + syllables[stress_index]
    return '.'.join(syllables)
