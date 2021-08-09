import unicodedata
import ipa_transcriber as t
import pytest


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


def test_transcribe_chandrabindus_and_anuswaras_final_m():
    chars = ["DEVANAGARI LETTER E", "DEVANAGARI LETTER VA", 'ə', "DEVANAGARI SIGN ANUSVARA"]
    expected = ['DEVANAGARI LETTER E', 'DEVANAGARI LETTER VA', '̃əm']
    actual = t.transcribe_chandrabindus_and_anuswaras(chars)
    assert actual == expected


def test_transcribe_chandrabindus_and_anuswaras_final_vowel_nasalised():
    chars = ["DEVANAGARI LETTER MA", 'DEVANAGARI VOWEL SIGN E', "DEVANAGARI SIGN ANUSVARA"]
    expected = ['DEVANAGARI LETTER MA', '̃eː']
    actual = t.transcribe_chandrabindus_and_anuswaras(chars)
    assert actual == expected


def test_transcribe_chandrabindus_and_anuswaras_medial_anusvara():
    chars = ["DEVANAGARI LETTER HA", 'DEVANAGARI VOWEL SIGN I', "DEVANAGARI SIGN ANUSVARA", "DEVANAGARI LETTER DA",
             'DEVANAGARI VOWEL SIGN II']
    expected = ['DEVANAGARI LETTER HA', '̃ɪn', "DEVANAGARI LETTER DA", 'DEVANAGARI VOWEL SIGN II']
    actual = t.transcribe_chandrabindus_and_anuswaras(chars)
    assert actual == expected


def test_transcribe_chandrabindus_and_anuswaras_medial_chandrabindu():
    chars = ["DEVANAGARI LETTER SA", 'DEVANAGARI VOWEL SIGN AA', "DEVANAGARI SIGN CANDRABINDU", "DEVANAGARI LETTER PA"]
    expected = ['DEVANAGARI LETTER SA', '̃aː', "DEVANAGARI LETTER PA"]
    actual = t.transcribe_chandrabindus_and_anuswaras(chars)
    assert actual == expected


def test_transcribe_chandrabindus_and_anuswaras_medial_chandrabindu_vowel():
    text = "कुँआ"
    chars = [unicodedata.name(c) for c in text]
    expected = ['DEVANAGARI LETTER KA', '̃ʊ', 'DEVANAGARI LETTER AA']
    actual = t.transcribe_chandrabindus_and_anuswaras(chars)
    assert actual == expected


def test_transcribe_chandrabindus_and_anuswaras_final_chandrabindu():
    text = "चिड़ियाँ"
    chars = [unicodedata.name(c) for c in text]
    expected = chars
    expected[-1] = '̃aː'
    actual = t.transcribe_chandrabindus_and_anuswaras(chars)
    assert actual == expected


def test_transcribe_chandrabindus_and_anuswaras_invalid():
    chars = ["DEVANAGARI LETTER SA",  "DEVANAGARI SIGN CANDRABINDU", "DEVANAGARI LETTER PA"]
    with pytest.raises(ValueError):
        t.transcribe_chandrabindus_and_anuswaras(chars)


def test_add_schwas():
    text = "कम"
    expected = ['DEVANAGARI LETTER KA', 'ə', 'DEVANAGARI LETTER MA', 'ə']
    names = [unicodedata.name(c) for c in text]
    actual = t.add_schwas(names)
    assert actual == expected


def test_add_schwas_halant():
    text = "रक्"
    expected = ['DEVANAGARI LETTER RA', 'ə', 'DEVANAGARI LETTER KA']
    names = [unicodedata.name(c) for c in text]
    actual = t.add_schwas(names)
    assert actual == expected


def test_syncopate_schwas_word_final():
    names = ['DEVANAGARI LETTER MA', 'ə', 'DEVANAGARI LETTER NA', 'ə']
    expected = ['DEVANAGARI LETTER MA', 'ə', 'DEVANAGARI LETTER NA']
    actual = t.syncopate_schwas(names)
    assert actual == expected


def test_syncopate_schwas_word_medial():
    names = ['DEVANAGARI LETTER HA', 'ə', 'DEVANAGARI LETTER RA', 'ə', 'DEVANAGARI LETTER KA', 'ə',
             'DEVANAGARI LETTER TA', 'ə']
    expected = ['DEVANAGARI LETTER HA', 'ə', 'DEVANAGARI LETTER RA', 'DEVANAGARI LETTER KA', 'ə', 'DEVANAGARI LETTER TA']
    actual = t.syncopate_schwas(names)
    assert actual == expected


def test_syncopate_schwas_short():
    names = ['DEVANAGARI LETTER KA', 'ə']
    expected = ['DEVANAGARI LETTER KA', 'ə']
    actual = t.syncopate_schwas(names)
    assert actual == expected


def test_nasal_place_assimilation():
    text = "anpanfant̪anɖʱanjanganɢ"
    expected = "ampamfant̪aɳɖʱaɲjaŋgaɴɢ"
    actual = t.assimilate_nasal_place(text)
    assert actual == expected


def test_add_syllable_boundaries_monosyllabic():
    text = "sər"
    expected = "sər"
    actual = t.add_syllable_boundaries(text)
    assert actual == expected


def test_add_syllable_boundaries_long_vowels():
    text = "meːraː"
    expected = "meː.raː"
    actual = t.add_syllable_boundaries(text)
    assert actual == expected


def test_add_syllable_boundaries_geminate():
    text = "pənnaː"
    expected = "pən.naː"
    actual = t.add_syllable_boundaries(text)
    assert actual == expected


def test_add_syllable_boundaries_double_cluster():
    text = "sətjə"
    expected = "sət.jə"
    actual = t.add_syllable_boundaries(text)
    assert actual == expected


def test_add_syllable_boundaries_triple_cluster():
    text = "vəst̪rəm"
    expected = "vəs.t̪rəm"
    actual = t.add_syllable_boundaries(text)
    assert actual == expected


def test_add_syllable_boundaries_final_cluster():
    text = "əŋk"
    expected = "əŋk"
    actual = t.add_syllable_boundaries(text)
    assert actual == expected


def test_add_syllable_boundaries_polysyllabic():
    text = "nɪrənt̪əraːnd̪ʱəkaːrɪt̪"
    expected = "nɪ.rən.t̪ər.aːn.d̪ʱə.kaː.rɪt̪"
    actual = t.add_syllable_boundaries(text)
    assert actual == expected


def test_transcribe_ipa():
    text = "प्रणाम मेरा नाम और अंक नमकीन हैं "
    expected = "prə.ɳaːm meː.raː naːm ɔːr ̃əŋk nəm.kiːn ɦ̃ɛː"
    actual = t.transcribe_to_ipa(text)
    assert actual == expected

