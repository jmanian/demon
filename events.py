import json
import logging
import os
# import re
from slackclient import SlackClient

logger = logging.getLogger()
logger.setLevel(logging.INFO)

expected_token = os.environ['VERIFICATION_TOKEN']
sc = SlackClient(os.environ['BOT_ACCESS_TOKEN'])

def lambda_handler(event, context):
    logger.info("Event received: %s", event)
    body = json.loads(event['body'])

    if body['token'] != expected_token:
        return empty_response(401)

    if body['type'] == 'url_verification':
        return verification_response(body)

    channel = body['event']['channel']
    if channel[0] == 'D'
        text = body['event']['text']
        sc.api_call("chat.postMessage", channel=channel, text=text)

    return empty_response(200)

def empty_response(code):
    return {
        'statusCode': code,
        'body': None,
        'headers': {
            'Content-Type': 'application/json'
        }
    }

def verification_response(body):
    return {
        'statusCode': 200,
        'body': body['challenge'],
        'headers': {
            'Content-Type': 'application/json'
        },
    }
