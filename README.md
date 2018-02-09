# 🤖 Slack Serverless Reaction Bot
It is a serverless BOT that responds to Slack's specific Reaction and responds with lot of Reactions.

***DEMO:***

![demo2](https://user-images.githubusercontent.com/1152469/35921649-9e76acbc-0c5e-11e8-85c3-346585669371.gif)

## Description
Using Slack's BOT and Subscribe to receive all the reactions toward Lambda via API-Gateway.
If there includes a specific reaction, call the Slack API and react back to the same message.
Slack BOT needs to be create manually, but AWS side automates environment construction by using Serverless Framework.

## Requirement
- AWS Account
- Serverless Framework
- Slack Account

## Installation
1. Create Slack BOT from [Here](https://api.slack.com/slack-apps)
    - Bot User
        - Display Name
        - Default Username
    - Permissions
        - OAuth & Permissions
            - Scopes
                - channels:history
                - channels:write
2. Get two tokens
    - Permissions
        - OAuth & Permissions
            - OAuth Access Token
            - Bot User OAuth Access Token

3. Clone this repo.
```
$ git clone https://github.com/saitota/SlackServerlessReactionBot.git
```

4. Modify sererless.yml 's two TOKEN to your token.
``` sererless.yml
OAUTH_TOKEN: 'xoxp-000000000000-000000000000-000000000000-0x0x0x0x0x0x0x0x0x0x0x0x0x0x0x0x'
BOT_TOKEN: 'xoxb-000000000000-0x0x0x0x0x0x0x'
```

5. Deploy with Serverless Framework (you must aws-cli initialize before)
```
$ sls deploy ./SlackServerlessReactionBot
...
api keys:
  None
endpoints:
  POST - https://0x0x0x0x0x.execute-api.ap-northeast-1.amazonaws.com/prod/
functions:
  fnc: SlackServerlessReactionBot-prod-fnc
```
6. Set Slack BOT endpoint and event subscribe settings 
    - Event Subscriptions
        - Request URL: `set your endopint url(you can see in your deploy log)`
    - Subscribe to Workspace Events
        - reaction_added
        - reaction_removed

7. Done! try to add Reaction at `HOOK_REACTION` (👍 is the default)

# 🤔 Anything Else
I wrote article about this BOT.

[ポするとプテピピックするサーバレスBOTを作った - Qiita](https://qiita.com/9c088bde87b9367f5414)

# 🐑 Author
[saitotak](https://qiita.com/saitotak)

# ✍ License
[MIT](./LICENSE)

