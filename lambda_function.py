import json
import logging
import os
import re

from base64 import b64decode
from urlparse import parse_qs

expected_token = os.environ['slackToken']

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def respond(err, text=None, username=None, icon_url=None):
    body = {
        'text': text,
        'username': username,
        'icon_url': icon_url
    }

    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(body),
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def icon_url(filename):
    return "https://jmanian.github.io/demon/icons/%s" % filename

def lambda_handler(event, context):
    logger.info("Event received: %s", event)
    params = parse_qs(event['body'].encode('ascii'))
    token = params['token'][0]
    if token != expected_token:
        logger.error("Request token (%s) does not match expected", token)
        return respond(Exception('Invalid request token'))

    if 'text' not in params:
        return respond(None, "")

    user_id = params['user_id'][0]
    text = params['text'][0]
    if user_id != 'USLACKBOT':
        if re.search(r"\bgreat(er|est)?\b", text, re.I) != None:
            word = "hug"
            match = re.search(r"\bgreat(?:er|est)?\b (\S+)", text, re.I)
            if match:
                word = match.group(1)
            text = "Ah, the greatest %s!" % word
            username = "grill_vogel"
            return respond(None, text, username, icon_url("grill_vogel.jpg"))
        if re.compile(r"\bbingo\b", re.I).search(text) != None:
            text = "Bingo, bye-bye!"
            username = 'peach'
            return respond(None, text, username, icon_url("peach.png"))

    return respond(None, "")
