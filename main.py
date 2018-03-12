import json
import logging
import urllib.request
import os

print('Loading function... ')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def event_to_json(event):
    if 'body' in event:
        body = json.loads(event.get('body'))
        return body
    elif 'token' in event:
        body = event
        return body
    else:
        logger.error('unexpected event format')
        exit


class ChallangeJson(object):
    def data(self, key):
        return {
            'isBase64Encoded': 'true',
            'statusCode': 200,
            'headers': {},
            'body': key
        }


def handler(event, context):
    #getenv
    OAUTH_TOKEN = os.environ['OAUTH_TOKEN']
    BOT_TOKEN = os.environ['BOT_TOKEN']
    #HOOK_REACTION = os.environ['HOOK_REACTION']
    HOOK_REACTIONS = os.environ['HOOK_REACTIONS']
    # Output the received event to the log
    logging.info(json.dumps(event))
    body = event_to_json(event)
    # return if it was challange-event
    if 'challenge' in body:
        challenge_key = body.get('challenge')
        logging.info('return challenge key %s:', challenge_key)
        return ChallangeJson().data(challenge_key)
    # define reaction
    emojis = HOOK_REACTIONS.split(',')
    if body.get('event').get('reaction') in emojis:
        logger.info('hit: %s', body.get('event').get('reaction'))

        headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'Authorization': 'Bearer {0}'.format(BOT_TOKEN)
        }

        # added 1st reaction
        if body.get('event').get('type') == 'reaction_added':
            url = 'https://slack.com/api/reactions.add'
            if body.get('event').get('reaction') == emojis[0] and body.get(
                    'event').get('user', '') != 'U9KRXEKLG':
                logger.info('human added 1st reaction')
                print('set 1st emoji')
                print(emojis[1])
                data = {
                    'token': OAUTH_TOKEN,
                    'channel': body.get('event').get('item').get('channel'),
                    'timestamp': body.get('event').get('item').get('ts'),
                    'name': emojis[1]
                }
            if body.get('event').get('reaction') in emojis and body.get(
                    'event').get('reaction') != emojis[0] and body.get(
                        'event').get('user', '') == 'U9KRXEKLG':
                logger.info('bot added 2st or later reaction')
                last_count = len(emojis) - 1
                this_count = emojis.index(body.get('event').get('reaction'))
                if (this_count != last_count):
                    logger.info('add: %s', emojis[this_count + 1])
                    data = {
                        'token': OAUTH_TOKEN,
                        'channel':
                        body.get('event').get('item').get('channel'),
                        'timestamp': body.get('event').get('item').get('ts'),
                        'name': emojis[this_count + 1]
                    }
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode('utf-8'),
                method='POST',
                headers=headers)
            res = urllib.request.urlopen(req)
            logger.info('post result: %s', res.msg)
        elif body.get('event').get('type') == 'reaction_removed' and body.get(
                'event').get('reaction') in emojis[0]:
            logger.info('human removed 1st reaction')
            url = 'https://slack.com/api/reactions.remove'
            for e in emojis:
                logger.info('remove: %s', e)
                data = {
                    'token': OAUTH_TOKEN,
                    'channel': body.get('event').get('item').get('channel'),
                    'timestamp': body.get('event').get('item').get('ts'),
                    'name': e
                }
                # remove処理
                req = urllib.request.Request(
                    url,
                    data=json.dumps(data).encode('utf-8'),
                    method='POST',
                    headers=headers)
                res = urllib.request.urlopen(req)
                logger.info('post result: %s', res.msg)
        return {'statusCode': 200, 'body': 'ok'}
    return {'statusCode': 200, 'body': 'quit'}
