# 🤖 Slack Reaction Bot
Slack の特定の Reaction に反応し、Reactionで反応し返してくれるサーバレスBOTです。

***DEMO:***

![demo2](https://user-images.githubusercontent.com/1152469/35921649-9e76acbc-0c5e-11e8-85c3-346585669371.gif)

## Description
Slack の BOT と Subscribe を使うことで、全ての Reaction を API-Gateway 経由で Lambda に受信します。
特定の Reaction だった場合は Slack API を呼び出して、Reaction を複数つけ返します。
Slack BOT は手動で設定する必要がありますが、AWS 側は Serverless Framework を使うことで環境構築を自動化しています。

## Requirement
- AWS アカウント
- Serverless Framework
- [serverless-plugin-aws-alerts](https://serverless.com/blog/serverless-ops-metrics/) (optional)
- Slack アカウント

## Installation
1. [ここ](https://api.slack.com/slack-apps) からBOT作成
    - Bot User
        - Display Name
        - Default Username
    - Permissions
        - OAuth & Permissions
            - Scopes
                - channels:history
                - channels:write
                
2. トークンを２つ取得
    - Permissions
        - OAuth & Permissions
            - OAuth Access Token
            - Bot User OAuth Access Token

3. リポジトリをClone
```
$ git clone https://github.com/saitota/SlackReactionBot.git
```

4. Serverless の設定ファイルを編集、先程のトークンで書き換えてください
``` environment_dev.yml
OAUTH_TOKEN: 'xoxp-000000000000-000000000000-000000000000-0x0x0x0x0x0x0x0x0x0x0x0x0x0x0x0x'
BOT_TOKEN: 'xoxb-000000000000-0x0x0x0x0x0x0x'
```

5. Serverless Framework でデプロイ (事前にaws-cliの初期設定が必要です)
```
$ sls deploy ./SlackReactionBot
...
api keys:
  None
endpoints:
  POST - https://0x0x0x0x0x.execute-api.ap-northeast-1.amazonaws.com/dev/
functions:
  fnc: SlackReactionBot-dev-fnc
```
6. Slack BOT のエンドポイント設定と、Subscribe設定をします
    - Event Subscriptions
        - Request URL: `set your endopint url(you can see in your deploy log)`
    - Subscribe to Workspace Events
        - reaction_added
        - reaction_removed

7. 設定完了！Slackで `HOOK_REACTIONS` の1stリアクション（デフォルトは1️⃣）をつけてみましょう

# 🤔 Anything Else
この BOT に関する記事を書きました。

[ポするとプテピピックするサーバレスBOTを作りました - Qiita](https://qiita.com/saitotak/items/9c088bde87b9367f5414)

# 🐑 Author
[saitotak](https://qiita.com/saitotak)

# ✍ License
[MIT](./LICENSE)

