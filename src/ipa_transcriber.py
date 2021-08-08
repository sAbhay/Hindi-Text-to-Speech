import unicodedata
from constants import *
import logging


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
        chars = transcribe_chandrabindus(chars)
        logging.debug(f"Chandrabindus: {chars}")

        for i, c in enumerate(chars):
            if c in UNICODE_TO_IPA:
                ipa_word += UNICODE_TO_IPA[c]
            else:
                if "DEVANAGARI" in c:
                    raise Exception(f"unhandled character at position {i}: {c}")

                # already converted in earlier steps
                ipa_word += c
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
            cleaned[-1] = UNICODE_TO_IPA[charnames[i-1]] + UNICODE_TO_IPA[charnames[i+1]]
            i += 2
            continue

        cleaned.append(charnames[i])
        i += 1
    cleaned += charnames[-1:]
    return cleaned


def transcribe_visargas(charnames: list) -> list:
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
            elif charnames[i] == 'DEVANAGARI LETTER KHA':
                cleaned[-1] = 'ʒ'
            i += 2
        i += 1
    cleaned += charnames[-1:]
    return cleaned


def add_schwas(charnames: list) -> list:
    cleaned = []
    for i in range(len(charnames)):
        cleaned.append(charnames[i])
        if ("LETTER" in charnames[i] and "VOWEL" not in charnames[i]) or charnames[i] not in UNICODE_TO_IPA:
            if i == len(charnames)-1:
                cleaned.append('ə')
            elif "VOWEL" not in charnames[i+1] or charnames[i+1] not in UNICODE_TO_IPA:
                cleaned.append('ə')
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

def transcribe_chandrabindus(chars: list) -> list:
    cleaned = [chars[0]]
    i = 1
    while i < len(chars):
        if chars[i] == 'DEVANAGARI SIGN CANDRABINDU':
            nasalized = ""
            if chars[i-1] == 'ə':
                nasalized = "̃" + 'ə'
            elif "VOWEL" in chars[i-1]:
                nasalized = '̃' + UNICODE_TO_IPA[chars[i-1]]
            else:
                raise ValueError(f"invalid input, non-vowel {chars[i-1]} precedes chandrabindu")
            del cleaned[-1]
            cleaned.append(nasalized)
            i += 1
            continue
        cleaned.append(chars[i])
        i += 1
    return cleaned
