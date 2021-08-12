import ipa_transcriber as t
import json

print(t.transcribe_to_ipa("प्रणाम"))


def lambda_handler(event, context):
    ipa = t.transcribe_to_ipa(event.body)
    return {
        'statusCode': 200,
        'body': json.dumps(ipa)
    }
