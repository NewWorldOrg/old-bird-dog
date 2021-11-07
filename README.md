# old bird dog

## 環境構築について

pypa/pipenv: Python Development Workflow for Humans. : https://github.com/pypa/pipenv

## 最初にすること

```bash
$ pwd
/hoge/fuga/old-bird-dog

# APIキーを設定する（すでに設定している場合は省略する）

$ cp config.sample.ini config.ini
$ vim config.ini

# 依存パッケージのインストール

$ pipenv install
```

## 使い方

```bash
$ pwd
/hoge/fuga/old-bird-dog

$ pipenv shell

# フォロワーの取得
$ python main.py -u AbeShinzo -type id

# フォロワーの詳細情報を取得
$ python main.py -u AbeShinzo -type detail -s ./output/[前の工程で生成されたCSVファイル]
```

## memo

python-twitter 3.4.2 documentation : https://python-twitter.readthedocs.io/en/latest/

GET followers/ids — Twitter Developers : https://developer.twitter.com/en/docs/accounts-and-users/follow-search-get-users/api-reference/get-followers-ids.html

Ratelimit 15min 15
Specifies the number of IDs attempt retrieval of, up to a maximum of 5,000 per distinct request.

GET users/lookup — Twitter Developers : https://developer.twitter.com/en/docs/accounts-and-users/follow-search-get-users/api-reference/get-users-lookup.html

Ratelimit 15min 900
user IDs up to 100 are allowed in a single request.
