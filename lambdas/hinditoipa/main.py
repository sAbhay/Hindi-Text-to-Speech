import sys
sys.path.insert(0, "src")

import logging
import ipa_transcriber as t


logging.basicConfig(level=logging.DEBUG)


def lambda_handler(event, context):
    logging.debug(f"event: {event}")
    ipa = t.transcribe_to_ipa(event["body"])
    logging.debug(ipa)
    return {
        'statusCode': 200,
        'body': ipa
    }
