import unicodedata
import ipa_transcriber as t

def test_transcribe_viramas():
    text = "क्रम"
    expected = ["kr", 'DEVANAGARI LETTER MA']
    names = [unicodedata.name(c) for c in text]
    actual = t.transcribe_viramas(names)
    assert actual == expected
