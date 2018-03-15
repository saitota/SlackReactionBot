import json
import logging
import urllib.request
import os

print('Loading function... ')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def event_to_dict(event):
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

class PostData(object):
    def __init__(self):
        self.BOT_TOKEN = os.environ['BOT_TOKEN']
        self.OAUTH_TOKEN = os.environ['OAUTH_TOKEN']

    def headers(self):
        return {
            'Content-Type': 'application/json; charset=UTF-8',
            'Authorization': 'Bearer {0}'.format(self.BOT_TOKEN)
        }

    def data(self, channel,ts,emoji):
        return {
            'token': self.OAUTH_TOKEN,
            'channel': channel,
            'timestamp': ts,
            'name': emoji
        }

def handler(event, context):
    #getenv
    HOOK_REACTIONS = os.environ['HOOK_REACTIONS']
    # Output the received event to the log
    logging.info(json.dumps(event))
    body = event_to_dict(event)

    # return if it was challange-event
    if 'challenge' in body:
        challenge_key = body.get('challenge')
        logging.info('return challenge key %s:', challenge_key)
        return ChallangeJson().data(challenge_key)

    # define reaction
    emojis = HOOK_REACTIONS.split(',')

    if body.get('event').get('reaction') in emojis:
        logger.info('hit: %s', body.get('event').get('reaction'))

        postdata = PostData()

        # added 1st reaction
        if body.get('event').get('type') == 'reaction_added':
            # 1st emoji has added 
            if body.get('event').get('reaction') == emojis[0] and body.get(
                    'event').get('user', '') != 'U9KRXEKLG':

                logger.info('1st emoji has added, set 2nd emoji: %s', emojis[1])
                post_head = postdata.headers()
                post_data = postdata.data(body.get('event').get('item').get('channel'),body.get('event').get('item').get('ts'),emojis[1])
            
            # the 2nd and the subsequent emoji has added 
            if body.get('event').get('reaction') in emojis and body.get(
                    'event').get('reaction') != emojis[0] and body.get(
                        'event').get('user', '') == 'U9KRXEKLG':

                logger.info('the 2nd and the subsequent emoji has added')
                last_count = len(emojis) - 1
                this_count = emojis.index(body.get('event').get('reaction'))
                if (this_count != last_count):
                    logger.info('bot will add: %s', emojis[this_count + 1])
                    post_head = postdata.headers()
                    post_data = postdata.data(body.get('event').get('item').get('channel'),body.get('event').get('item').get('ts'),emojis[this_count + 1])

            print(json.dumps(post_head))
            print(json.dumps(post_data))
            url = 'https://slack.com/api/reactions.add'
            req = urllib.request.Request(
                url,
                data=json.dumps(post_data).encode('utf-8'),
                method='POST',
                headers=post_head)
            res = urllib.request.urlopen(req)
            logger.info('post result: %s', res.msg)

        # 1st emoji has removed
        elif body.get('event').get('type') == 'reaction_removed' and body.get(
                'event').get('reaction') in emojis[0]:

            logger.info('1st emoji has removed')
            url = 'https://slack.com/api/reactions.remove'
            for emoji in emojis:
                logger.info('remove: %s', emoji)

                post_head = postdata.headers()
                post_data = postdata.data(body.get('event').get('item').get('channel'),body.get('event').get('item').get('ts'),emoji)

                print(json.dumps(post_head))
                print(json.dumps(post_data))

                req = urllib.request.Request(
                    url,
                    data=json.dumps(post_data).encode('utf-8'),
                    method='POST',
                    headers=post_head)
                    
                res = urllib.request.urlopen(req)
                logger.info('post result: %s', res.msg)

        return {'statusCode': 200, 'body': 'ok'}
    return {'statusCode': 200, 'body': 'quit'}
