import json
import logging
import os
import re
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

        if 'text' in event:
            channel = event['channel']
            text = event['text']
            thread_ts = event.get('thread_ts')

            # Grill Vogel
            if re.search(r"\bgreat(er|est)?\b", text, re.I) != None:
                word = "hug"
                match = re.search(r"\bgreat(?:er|est)?\b (\S+)", text, re.I)
                if match:
                    word = match.group(1)
                post_text = "Ah, the greatest %s!" % word
                username = "Grill Vogel"
                post_message(channel, thread_ts, post_text, username, "grill_vogel.jpg")

            # Peach
            if re.search(r"\bbingo\b", text, re.I) != None:
                post_text = "Bingo, bye-bye!"
                username = 'Peach'
                post_message(channel, thread_ts, post_text, username, "peach.png")

def post_message(channel, thread_ts, text, username, icon_name):
    if thread_ts == None:
        sc.api_call(
            "chat.postMessage",
            channel=channel,
            text=text,
            as_user=False,
            username=username,
            icon_url=icon_url(icon_name)
        )
    else:
        sc.api_call(
            "chat.postMessage",
            channel=channel,
            text=text,
            thread_ts=thread_ts,
            as_user=False,
            username=username,
            icon_url=icon_url(icon_name)
        )

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

# files go in icons/
def icon_url(filename):
    return "https://jmanian.github.io/demon/icons/%s" % filename
