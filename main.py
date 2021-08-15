import sys
sys.path.insert(0, "./src")

import logging
import ipa_transcriber as t


logging.basicConfig(level=logging.DEBUG)
print(t.transcribe_to_ipa("प्रणाम"))

# Retrieve the logger instance
logger = logging.getLogger()


def lambda_handler(event, context):
    logger.debug(f"event: {event}")
    ipa = t.transcribe_to_ipa(event["body"])
    logger.debug(ipa)
    return {
        'statusCode': 200,
        'body': ipa
    }
