import json
import logging
import os
# import re

expected_token = os.environ['VERIFICATION_TOKEN']

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info("Event received: %s", event)
    body = json.loads(event['body'])

    if body['token'] != expected_token:
        return {
            'statusCode': 401,
            'body': None
        }

    if body['type'] == 'url_verification':
        return {
            'statusCode': 200,
            'body': body['challenge'],
            'headers': {
                'Content-Type': 'application/json'
            },
        }
    else:
        return {
            'statusCode': 200,
            'body': None,
            'headers': {
                'Content-Type': 'application/json'
            }
        }
