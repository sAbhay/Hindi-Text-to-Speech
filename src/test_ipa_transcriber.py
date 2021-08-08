import unicodedata
import ipa_transcriber as t


def test_transcribe_viramas_word_initial():
    text = "क्रम"
    expected = ["kr", 'DEVANAGARI LETTER MA']
    names = [unicodedata.name(c) for c in text]
    actual = t.transcribe_viramas(names)
    assert actual == expected

def test_transcribe_viramas_word_final():
    text = "पत्र"
    expected = ["DEVANAGARI LETTER PA", 't̪r']
    names = [unicodedata.name(c) for c in text]
    actual = t.transcribe_viramas(names)
    assert actual == expected


def test_transcribe_viramas_sequential():
    text = "द्रक्षों"
    expected = ['d̪r', 'kʂ', 'DEVANAGARI VOWEL SIGN O', 'DEVANAGARI SIGN ANUSVARA']
    names = [unicodedata.name(c) for c in text]
    actual = t.transcribe_viramas(names)
    assert actual == expected


def test_transcribe_viramas_multi_cluster():
    text = "चन्द्र"
    expected = ['DEVANAGARI LETTER CA', "nd̪r"]
    names = [unicodedata.name(c) for c in text]
    actual = t.transcribe_viramas(names)
    assert actual == expected

def test_transcribe_viramas_gya():
    text = "ज्ञान"
    expected = ['gj', 'DEVANAGARI VOWEL SIGN AA', 'DEVANAGARI LETTER NA']
    names = [unicodedata.name(c) for c in text]
    actual = t.transcribe_viramas(names)
    assert actual == expected

def test_transcribe_viramas_short():
    text = "क्"
    # halant cases are handled by add_schwas
    expected = ['DEVANAGARI LETTER KA', 'DEVANAGARI SIGN VIRAMA']
    names = [unicodedata.name(c) for c in text]
    actual = t.transcribe_viramas(names)
    assert actual == expected

def test_transcribe_visarga_word_final_consonant():
    text = "नमः"
    chars = [unicodedata.name(c) for c in text]
    expected = ['DEVANAGARI LETTER NA', 'DEVANAGARI LETTER MA', 'əhə']
    actual = t.transcribe_visargas(chars)
    assert actual == expected

def test_transcribe_visarga_word_final_schwa():
    text = "नमः"
    chars = [unicodedata.name(c) for c in text]
    chars.insert(-1, 'ə')
    expected = ['DEVANAGARI LETTER NA', 'DEVANAGARI LETTER MA', 'ə', 'hə']
    actual = t.transcribe_visargas(chars)
    assert actual == expected

def test_transcribe_visarga_word_final_long_vowel():
    text = "वाः"
    chars = [unicodedata.name(c) for c in text]
    expected = ['DEVANAGARI LETTER VA', 'aːha']
    actual = t.transcribe_visargas(chars)
    assert actual == expected

def test_transcribe_visarga_medial():
    text = "दुःख"
    chars = [unicodedata.name(c) for c in text]
    expected = ['DEVANAGARI LETTER DA', 'ʊh', 'DEVANAGARI LETTER KHA']
    actual = t.transcribe_visargas(chars)
    assert actual == expected

def test_transcribe_nuktas_kh():
    text = "ख़"
    chars = [unicodedata.name(c) for c in text]
    expected = ['x']
    actual = t.transcribe_nuktas(chars)
    assert actual == expected

def test_transcribe_nuktas_zh():
    text = "झ़"
    chars = [unicodedata.name(c) for c in text]
    expected = ['ʒ']
    actual = t.transcribe_nuktas(chars)
    assert actual == expected

def test_transcribe_nuktas_non_final():
    text = "ख़ून"
    chars = [unicodedata.name(c) for c in text]
    expected = ['x', 'DEVANAGARI VOWEL SIGN UU', 'DEVANAGARI LETTER NA']
    actual = t.transcribe_nuktas(chars)
    assert actual == expected
