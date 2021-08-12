import ipa_transcriber as t
import json

vowels = "क का कि की के कै कु कू को कौ कं काँ कः कृ "
vowel_letters = "अ आ इ ई ए ऐ उ ऊ ओ औ ऋ "
consonants = "क ख ग घ ङ ह च छ ज झ ञ य श ट ठ ड ढ ड़ ढ़ ण र ष त थ द ध न ल स प फ ब भ म व "
loans = "क़ ख़ ग़ ज़ झ़ फ़ "
conjunctions = "ज्ञ क्ष त्र श्र "
virama = "क्र क् "
sample_text = "प्रणाम मेरा नाम नमकीन है"
text = sample_text

def lambda_handler(event, context):
    ipa = t.transcribe_to_ipa(event.body)
    return {
        'statusCode': 200,
        'body': json.dumps(ipa)
    }
