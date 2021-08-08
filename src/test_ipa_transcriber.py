import unicodedata
import ipa_transcriber as t

def test_transcribe_viramas():
    text = "क्रम"
    expected = ["kr", 'DEVANAGARI LETTER MA']
    names = [unicodedata.name(c) for c in text]
    actual = t.transcribe_viramas(names)
    assert actual == expected

def test_transcribe_viramas_sequential():
    text = "द्रक्ष"
    expected = ['d̪r', 'kʂ']
    names = [unicodedata.name(c) for c in text]
    actual = t.transcribe_viramas(names)
    assert actual == expected

def test_transcribe_viramas_multi_cluster():
    text = "चन्द्र"
    expected = ['DEVANAGARI LETTER CA', "nd̪r"]
    names = [unicodedata.name(c) for c in text]
    actual = t.transcribe_viramas(names)
    assert actual == expected
