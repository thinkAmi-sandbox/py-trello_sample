# py-trello_sample

## セットアップ
```
# 任意のGit用ディレクトリへ移動
>cd path\to\dir

# GitHubからカレントディレクトリへclone
path\to\dir>git clone https://github.com/thinkAmi-sandbox/Django_modelform_validation_sample.git

# virtualenv環境の作成とactivate
# *Python3.5は、`c:\python35-32\`の下にインストール
path\to\dir>virtualenv -p c:\python35-32\python.exe env
path\to\dir>env\Scripts\activate

# requirements.txtよりインストール
(env)path\to\dir>pip install -r requirements.txt

# 必要な定数を設定
TRELLO_API_KEY = ""
TRELLO_TOKEN = ""

BOARD_ID = ""
LIST_ID = ""
CARD_ID = ""


# 動作確認
## ボードまわり
(env)path\to\dir>python run.py boards

## リストまわり
(env)path\to\dir>python run.py lists

## カードまわり
(env)path\to\dir>python run.py cards

## コメントまわり
(env)path\to\dir>python run.py comment

## ファイル添付まわり
(env)path\to\dir>python run.py attachment

## チェックリストまわり
(env)path\to\dir>python run.py checklist

## Trello APIをfetch_json()で叩く
(env)path\to\dir>python run.py raw_api
```

　  
## テスト環境

- Windows10
- Python 3.5.1
- py-trello 0.4.3

　  
## 関係するブログ
[Python + py-trelloで、Trello APIを使ってみた - メモ的な思考的な](http://thinkami.hatenablog.com/entry/2016/03/01/003050)