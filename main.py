import json
import logging
import urllib.request
import os

print('Loading function... ')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    #getenv
    OAUTH_TOKEN = os.environ['OAUTH_TOKEN']
    BOT_TOKEN = os.environ['BOT_TOKEN']
    HOOK_REACTION = os.environ['HOOK_REACTION']
    ADD_REACTIONS = os.environ['ADD_REACTIONS']

    #受信したjsonをLogsに出力
    logging.info(json.dumps(event))
    # json処理
    if 'body' in event:
        body = json.loads(event.get('body'))
    elif 'token' in event:
        body = event
    else:
        logger.error('unexpected event format')
        return 'error'
    #url_verificationイベントに返す
    if 'challenge' in body:
        challenge = body.get('challenge')
        logging.info('return challenge key %s:', challenge)
        return {
            'isBase64Encoded': 'true',
            'statusCode': 200,
            'headers': {},
            'body': challenge
        }
    # 特定のリアクションだったら
    if body.get('event').get('reaction') == HOOK_REACTION:
        # add か remove か決める
        if body.get('event').get('type') == 'reaction_added':
            url = 'https://slack.com/api/reactions.add'
        elif  body.get('event').get('type') == 'reaction_removed':
            url = 'https://slack.com/api/reactions.remove'

        headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'Authorization': 'Bearer {0}'.format(BOT_TOKEN)
        }
        # reaction定義
        emoji = ADD_REACTIONS.split(',')
        for e in emoji:
            print( e)
            data = {
                'token': OAUTH_TOKEN,
                'channel': body.get('event').get('item').get('channel'),
                'timestamp': body.get('event').get('item').get('ts'),
                'name': e
            }
            # POST処理　
            req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), method='POST', headers=headers)
            res = urllib.request.urlopen(req)
            logger.info('post result: %s', res.msg)
        return {'statusCode': 200, 'body': 'ok'}
    return {'statusCode': 200, 'body': 'quit'}