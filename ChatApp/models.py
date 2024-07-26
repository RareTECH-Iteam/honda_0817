import pymysql
from util.DB import DB
from flask import abort
from flask_socketio import SocketIO

# FlaskアプリケーションとSocketIOの設定
socketio = SocketIO()  # Flaskアプリケーションと一緒にSocketIOを初期化します

class dbConnect:
    # ユーザー情報の追加
    def createUser(uid, username, email, password, address, greeting):
        try:
            conn = DB.getConnection()  # データベース接続を取得
            cur = conn.cursor()  # カーソルを作成
            sql = "INSERT INTO users (uid, username, email, password, address, greeting) VALUES (%s, %s, %s, %s, %s, %s);"  # SQLクエリを定義
            cur.execute(sql, (uid, username, email, password, address, greeting))  # クエリを実行
            conn.commit()  # トランザクションをコミット
        except Exception as e:
            print(e + 'が発生しています')  # エラーメッセージを出力
            abort(500)  # HTTP 500エラーを返す
        finally:
            cur.close()  # カーソルを閉じる

    # メールアドレスを指定してユーザー情報を取得
    def getUser(email):
        try:
            conn = DB.getConnection()  # データベース接続を取得
            cur = conn.cursor()  # カーソルを作成
            sql = "SELECT * FROM users WHERE email=%s;"  # SQLクエリを定義
            cur.execute(sql, (email))  # クエリを実行
            user = cur.fetchone()  # 結果を取得
            return user  # ユーザー情報を返す
        except Exception as e:
            print(e + 'が発生しています')  # エラーメッセージを出力
            abort(500)  # HTTP 500エラーを返す
        finally:
            cur.close()  # カーソルを閉じる

    # uidを指定してdetail.htmlに表示する
    def getUserByUid(uid):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()  # カーソルを作成
            sql = "SELECT * FROM users WHERE uid=%s;"
            cur.execute(sql, (uid,))
            user = cur.fetchone()
            return user
        except Exception as e:
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            cur.close()

    # ユーザー情報の更新
    def updateUser(uid, username, email, address, greeting):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "UPDATE users SET username=%s, email=%s, address=%s, greeting=%s WHERE uid=%s;"
            cur.execute(sql, (username, email, address, greeting, uid))
            conn.commit()
        except Exception as e:
            print(str(e) + 'が発生しました')
            abort(500)
        finally:
            cur.close()

    # チャットルーム一覧を取得するメソッド
    def getChatRoomList(uid):
        try:
            conn = DB.getConnection()  # データベース接続を取得
            cur = conn.cursor()  # カーソルを作成
            sql = "SELECT * FROM chat WHERE FIND_IN_SET(%s, user_ids);"
            cur.execute(sql, (uid,))  # クエリを実行
            chat_rooms = cur.fetchall()  # 結果を取得
            return chat_rooms  # チャットルームの一覧を返す
        except Exception as e:
            print(str(e) + 'が発生しました')  # エラーメッセージを出力
            abort(500)  # HTTP 500エラーを返す
        finally:
            cur.close()  # カーソルを閉じる

    # uidに紐づくメッセージを取得する処理
    def getMessageAll(cid):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT id,u.uid, user_name, message FROM messages AS m INNER JOIN users AS u ON m.uid = u.uid WHERE cid = %s;"
            cur.execute(sql, (cid))
            messages = cur.fetchall()
            return messages
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            cur.close()

    # uidに紐づくメッセージを作成する処理
    def createMessage(uid, cid, message):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO messages(uid, cid, message) VALUES(%s, %s, %s)"
            cur.execute(sql, (uid, cid, message))
            conn.commit()
            # メッセージ作成後にSocket.IOで通知を送信
            # socketio.emit('new_message', {'uid': uid, 'cid': cid, 'message': message})
        except Exception as e:
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            cur.close()

    # uidに紐づくメッセージを削除する処理
    # def deleteMessage(message_id):
    #     try:
    #         conn = DB.getConnection()
    #         cur = conn.cursor()
    #         sql = "DELETE FROM messages WHERE id=%s;"
    #         cur.execute(sql, (message_id))
    #         conn.commit()
    #     except Exception as e:
    #         print(e + 'が発生しています')
    #         abort(500)
    #     finally:
    #         cur.close()

    def getMessagesByChatRoom(chat_id, uid=None):
        try:
            conn = DB.getConnection()  # データベース接続を取得
            cur = conn.cursor()  # カーソルを作成

            # SQLクエリを定義（uidがある場合とない場合で条件を変更）
            if uid is not None:
                sql = "SELECT * FROM messages WHERE cid=%s AND uid=%s ORDER BY created_at;"
                params = (chat_id, uid)
            else:
                sql = "SELECT * FROM messages WHERE cid=%s ORDER BY created_at;"
                params = (chat_id,)

            cur.execute(sql, params)  # クエリを実行
            messages = cur.fetchall()  # 結果を全て取得
            return messages  # メッセージ一覧を返す

        except Exception as e:
            print(f"エラー: {str(e)}")  # エラーメッセージを出力
            abort(500)  # HTTP 500エラーを返す

        finally:
            cur.close()  # カーソルを閉じる
            conn.close()  # データベース接続を閉じる

    # # すべてのチャットを取得
    def getChatAll():
        try:
            conn = DB.getConnection()  # データベース接続を取得
            cur = conn.cursor()  # カーソルを作成
            sql = "SELECT * FROM chat;"  # SQLクエリを定義
            cur.execute(sql)  # クエリを実行
            chats = cur.fetchall()  # 結果を全て取得
            return chats  # チャット情報を返す
        except Exception as e:
            print(e + 'が発生しています')  # エラーメッセージを出力
            abort(500)  # HTTP 500エラーを返す
        finally:
            cur.close()  # カーソルを閉じる
























    # # チャットルームの追加
    # def addChatRoom(uid, chat_name, chat_description):
    #     try:
    #         conn = DB.getConnection()  # データベース接続を取得
    #         cur = conn.cursor()  # カーソルを作成
    #         sql = "INSERT INTO chat (uid, name, abstract) VALUES (%s, %s, %s);"  # SQLクエリを定義
    #         cur.execute(sql, (uid, chat_name, chat_description))  # クエリを実行
    #         conn.commit()  # トランザクションをコミット
    #     except Exception as e:
    #         print(str(e) + 'が発生しています')  # エラーメッセージを出力
    #         abort(500)  # HTTP 500エラーを返す
    #     finally:
    #         cur.close()  # カーソルを閉じる

    # # メッセージの追加
    # def addMessage(uid, cid, message):
    #     try:
    #         conn = DB.getConnection()  # データベース接続を取得
    #         cur = conn.cursor()  # カーソルを作成
    #         sql = "INSERT INTO messages (uid, cid, message) VALUES (%s, %s, %s);"  # SQLクエリを定義
    #         cur.execute(sql, (uid, cid, message))  # クエリを実行
    #         conn.commit()  # トランザクションをコミット
    #     except Exception as e:
    #         print(str(e) + 'が発生しています')  # エラーメッセージを出力
    #         abort(500)  # HTTP 500エラーを返す
    #     finally:
    #         cur.close()  # カーソルを閉じる

    # # チャットルームに関連するメッセージの取得
    # def getMessagesByChatRoom(uid, chat_id):
    #     try:
    #         conn = DB.getConnection()  # データベース接続を取得
    #         cur = conn.cursor()  # カーソルを作成
    #         sql = "SELECT * FROM messages WHERE cid=%s AND uid=%s ORDER BY created_at;"  # SQLクエリを定義
    #         cur.execute(sql, (chat_id, uid))  # クエリを実行
    #         messages = cur.fetchall()  # 結果を全て取得
    #         return messages  # メッセージ一覧を返す
    #     except Exception as e:
    #         print(str(e) + 'が発生しました')  # エラーメッセージを出力
    #         abort(500)  # HTTP 500エラーを返す
    #     finally:
    #         cur.close()  # カーソルを閉じる
            


    # # チャットIDを指定してチャット情報を取得
    # def getChatById(cid):
    #     try:
    #         conn = DB.getConnection()  # データベース接続を取得
    #         cur = conn.cursor()  # カーソルを作成
    #         sql = "SELECT * FROM chat WHERE id=%s;"  # SQLクエリを定義
    #         cur.execute(sql, (cid,))  # クエリを実行
    #         chat = cur.fetchone()  # 結果を取得
    #         return chat  # チャット情報を返す
    #     except Exception as e:
    #         print(e + 'が発生しています')  # エラーメッセージを出力
    #         abort(500)  # HTTP 500エラーを返す
    #     finally:
    #         cur.close()  # カーソルを閉じる

    # # チャット名を指定してチャット情報を取得
    # def getChatByName(chat_name):
    #     try:
    #         conn = DB.getConnection()  # データベース接続を取得
    #         cur = conn.cursor()  # カーソルを作成
    #         sql = "SELECT * FROM chat WHERE name=%s;"  # SQLクエリを定義
    #         cur.execute(sql, (chat_name,))  # クエリを実行
    #         chat = cur.fetchone()  # 結果を取得
    #         return chat  # チャット情報を返す
    #     except Exception as e:
    #         print(e + 'が発生しています')  # エラーメッセージを出力
    #         abort(500)  # HTTP 500エラーを返す
    #     finally:
    #         cur.close()  # カーソルを閉じる

    # # チャットの追加
    # def addChat(uid, newChatName, newChatDescription):
    #     try:
    #         conn = DB.getConnection()  # データベース接続を取得
    #         cur = conn.cursor()  # カーソルを作成
    #         sql = "INSERT INTO chat (uid, name, abstract) VALUES (%s, %s, %s);"  # SQLクエリを定義
    #         cur.execute(sql, (uid, newChatName, newChatDescription))  # クエリを実行
    #         conn.commit()  # トランザクションをコミット
    #     except Exception as e:
    #         print(e + 'が発生しています')  # エラーメッセージを出力
    #         abort(500)  # HTTP 500エラーを返す
    #     finally:
    #         cur.close()  # カーソルを閉じる

    # # チャット情報の更新
    # def updateChat(uid, newChatName, newChatDescription, cid):
    #     try:
    #         conn = DB.getConnection()  # データベース接続を取得
    #         cur = conn.cursor()  # カーソルを作成
    #         sql = "UPDATE chat SET uid=%s, name=%s, abstract=%s WHERE id=%s;"  # SQLクエリを定義
    #         cur.execute(sql, (uid, newChatName, newChatDescription, cid))  # クエリを実行
    #         conn.commit()  # トランザクションをコミット
    #     except Exception as e:
    #         print(e + 'が発生しました')  # エラーメッセージを出力
    #         abort(500)  # HTTP 500エラーを返す
    #     finally:
    #         cur.close()  # カーソルを閉じる

    # # チャットの削除
    # def deleteChat(cid):
    #     try:
    #         conn = DB.getConnection()  # データベース接続を取得
    #         cur = conn.cursor()  # カーソルを作成
    #         sql = "DELETE FROM chat WHERE id=%s;"  # SQLクエリを定義
    #         cur.execute(sql, (cid,))  # クエリを実行
    #         conn.commit()  # トランザクションをコミット
    #     except Exception as e:
    #         print(e + 'が発生しています')  # エラーメッセージを出力
    #         abort(500)  # HTTP 500エラーを返す
    #     finally:
    #         cur.close()  # カーソルを閉じる