
import sys
import os
import __main__
from datetime import datetime
from trello import TrelloClient

TRELLO_API_KEY = ""
TRELLO_TOKEN = ""

BOARD_ID = ""
LIST_ID = ""
CARD_ID = ""

def main():
    # APIクライアントを作成
    client = TrelloClient(TRELLO_API_KEY, 
                          token=TRELLO_TOKEN)
    
    params = sys.argv
    # index=0はファイル名が入っているので、削除
    params.pop(0)
    
    for p in params:
        f = getattr(__main__, p)
        f(client)
    
    
def boards(client):
    # ボードの作成
    created_board = client.add_board("APIで作ったボード")
    
    # ボードの一覧
    # closeしたボードも一覧に表示されるので注意
    boards = client.list_boards()
    for board in boards:
        print("board id: {id} {closed}".format(
            id=board.id, closed="(Closed)" if board.closed else ""))
        # nameにはバイト列が入ってるので、デコードする必要がある
        # http://qiita.com/FGtatsuro/items/f45c349e06d6df95839b
        print("board name: {}".format(board.name.decode("utf-8")))
    
    # APIでボードを作ると、デフォルトでは、"To Do" / "Doing" / "Done" の3つのリストができる
    lists = created_board.all_lists()
    for l in lists:
        print("list id: {}".format(l.id))
        print("list name: {}".format(l.name.decode("utf-8")))
    
    # 必要に応じてボードをClose
    is_archive = input("作成したボードをCloseする場合は、何か入力してEnterしてください > ")
    if is_archive:
        created_board.close()


def lists(client):
    # boardに対して処理を行う
    board = client.get_board(BOARD_ID)
    
    # リストの作成
    created_list = board.add_list("APIで作ったリスト")
    
    # ボードにあるリストの一覧
    # Archiveしたリストも表示されるので注意
    lists = board.all_lists()
    for l in lists:
        print("list id: {id} {closed}".format(
            id=l.id, closed="(Closed)" if l.closed else ""))
        print("list name: {}".format(l.name.decode("utf-8")))

    # 必要に応じてリストをArchive
    is_archive = input("作成したリストをアーカイブする場合は、何か入力してEnterしてください > ")
    if is_archive:
        created_list.close()


def cards(client):
    # listに対して処理を行うが、
    # 直接listを取得する方法が見当たらないため、boad > listの順に取得して処理を行う
    board = client.get_board(BOARD_ID)
    # listはPythonの関数名で存在するので、使うのを避ける
    target_list = board.get_list(LIST_ID)
    
    # カードの作成
    created_card = target_list.add_card("APIで作ったカード")
    
    # リストにあるカードの一覧
    # Archiveしたカードは表示されない
    cards = target_list.list_cards()
    for c in cards:
        print("card id: {}".format(c.id))
        print("card name: {}".format(c.name.decode("utf-8")))

    # 必要に応じてカードをArchive
    is_archive = input("作成したカードをアーカイブする場合は、何か入力してEnterしてください > ")
    if is_archive:
        created_card.set_closed(True)
        
    # 必要に応じてカードを削除する
    # GUIと異なり、Archiveしてなくても削除できる
    is_deletion = input("作成したカードを削除する場合は、何か入力してEnterしてください > ")
    if is_deletion:
        created_card.delete()


def comment(client):
    # cardに対して処理を行う
    card = client.get_card(CARD_ID)
    
    # コメントを追加
    card.comment(datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

    # コメントを表示
    comments = card.get_comments()
    for i, c in enumerate(comments):
        # JSONが辞書になって返ってきてることに注意
        print("comment No{no}: {comment}".format(
            no=i, comment=c["data"]["text"]))
        
    # コメントの削除メソッドは、ライブラリでは用意されていない
        
        
def attachment(client):
    # カードにファイルを添付
    card = client.get_card(CARD_ID)
    # https://twitter.com/hugorodgerbrown/status/307476541162532864
    # https://gist.github.com/hugorodgerbrown/5058032
    
    path = os.path.abspath(os.path.dirname(__file__))
    text_file_path = os.path.join(path, "attachment.txt")
    
    # バイナリモードで開く
    # http://docs.python-requests.org/en/latest/user/quickstart/#post-a-multipart-encoded-file
    text_file = open(text_file_path, "rb")
    
    # 半角英数のnameでは、そのファイル名になる
    # card.attach(name="attach1.txt", file=text_file)
    
    # nameに日本語を渡すと、"Upload"というファイル名になる
    card.attach(name="日本語.txt", file=text_file)
    
    # 試しに、nameにbyte列化した日本語を渡すとエラーになる
    # encoded_name = "日本語.txt".encode("utf-8")
    # card.attach(name=encoded_name, file=text_file)
    # => TypeError: a bytes-like object is required, not "str"


def checklist(client):
    # カードにチェックリストを追加
    card = client.get_card(CARD_ID)
    
    # 項目を2つ持つチェックリストを作成
    created_checklist = card.add_checklist("APIで作ったチェックリスト",
                                           ["アイテム1", "item2"])
    
    # チェックリストのアイテムにチェックを入れる
    created_checklist.set_checklist_item("アイテム1", True)
    
    # チェックリストを一覧表示
    # 削除されたチェックリストは表示されない
    # 直接扱えるメソッドが見当たらなかったため、一度fetchしてから取り出す
    card.fetch()
    for checklist in card.checklists:
        print("Checklist id：{id} / name: {name}".format(
            id=checklist.id, name=checklist.name))
            
        for i, item in enumerate(checklist.items):
            print("Item - index:{index} / id: {id} / name: {name} / checked: {checked}".format(
                index=i, id=item["id"], name=item["name"], checked=item["checked"]))
    
    # 必要に応じてチェックリストを削除
    is_deletion = input("作成したチェックリストを削除する場合は、何か入力してEnterしてください > ")
    if is_deletion:
        created_checklist.delete()


def raw_api(client):
    # py-trelloでは用意されていないTrello APIを試す
    # client.fetch_json()を使うと良い
    
    # 今回は、コメントの削除を試してみるので、まずはコメントを作成する
    comment(client)
    is_deletion = input("Enterを押すと続行します > ")
    
    # 最後のコメントを削除
    card = client.get_card(CARD_ID)
    last_comment = card.get_comments()[-1]
    
    # https://developers.trello.com/advanced-reference/card#delete-1-cards-card-id-or-shortlink-actions-idaction-comments
    client.fetch_json(
        "/cards/{card_id}/actions/{comment_id}/comments".format(
            card_id=card.id, comment_id=last_comment["id"]
        ),
        http_method="DELETE")


if __name__ == "__main__":
    main()