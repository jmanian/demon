import json
import logging
import os
# import re
from slackclient import SlackClient

logger = logging.getLogger()
logger.setLevel(logging.INFO)

expected_token = os.environ['VERIFICATION_TOKEN']
sc = SlackClient(os.environ['BOT_ACCESS_TOKEN'])
bot_id = os.environ['BOT_ID']
user_id = os.environ['USER_ID']

def lambda_handler(event, context):
    logger.info("Event received: %s", event)
    body = json.loads(event['body'])

    if body['token'] != expected_token:
        return empty_response(401)

    if body['type'] == 'url_verification':
        return verification_response(body)


    process_event(body['event'])

    return empty_response(200)

def process_event(event):
    if event['type'] == 'message':
        # don't respond to self
        if 'bot_id' in event and event['bot_id'] == bot_id:
            return
        if 'user' in event and event['user'] == user_id:
            return

        channel = event['channel']
        if channel[0] == 'D' and 'text' in event:
            text = event['text']
            sc.api_call("chat.postMessage", channel=channel, text=text, as_user=True)

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
