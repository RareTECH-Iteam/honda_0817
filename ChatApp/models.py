import pymysql
from util.DB import DB

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

    # すべてのチャットを取得
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

    # チャットIDを指定してチャット情報を取得
    def getChatById(cid):
        try:
            conn = DB.getConnection()  # データベース接続を取得
            cur = conn.cursor()  # カーソルを作成
            sql = "SELECT * FROM chat WHERE id=%s;"  # SQLクエリを定義
            cur.execute(sql, (cid,))  # クエリを実行
            chat = cur.fetchone()  # 結果を取得
            return chat  # チャット情報を返す
        except Exception as e:
            print(e + 'が発生しています')  # エラーメッセージを出力
            abort(500)  # HTTP 500エラーを返す
        finally:
            cur.close()  # カーソルを閉じる

    # チャット名を指定してチャット情報を取得
    def getChatByName(chat_name):
        try:
            conn = DB.getConnection()  # データベース接続を取得
            cur = conn.cursor()  # カーソルを作成
            sql = "SELECT * FROM chat WHERE name=%s;"  # SQLクエリを定義
            cur.execute(sql, (chat_name,))  # クエリを実行
            chat = cur.fetchone()  # 結果を取得
            return chat  # チャット情報を返す
        except Exception as e:
            print(e + 'が発生しています')  # エラーメッセージを出力
            abort(500)  # HTTP 500エラーを返す
        finally:
            cur.close()  # カーソルを閉じる

    # チャットの追加
    def addChat(uid, newChatName, newChatDescription):
        try:
            conn = DB.getConnection()  # データベース接続を取得
            cur = conn.cursor()  # カーソルを作成
            sql = "INSERT INTO chat (uid, name, abstract) VALUES (%s, %s, %s);"  # SQLクエリを定義
            cur.execute(sql, (uid, newChatName, newChatDescription))  # クエリを実行
            conn.commit()  # トランザクションをコミット
        except Exception as e:
            print(e + 'が発生しています')  # エラーメッセージを出力
            abort(500)  # HTTP 500エラーを返す
        finally:
            cur.close()  # カーソルを閉じる

    # チャット情報の更新
    def updateChat(uid, newChatName, newChatDescription, cid):
        try:
            conn = DB.getConnection()  # データベース接続を取得
            cur = conn.cursor()  # カーソルを作成
            sql = "UPDATE chat SET uid=%s, name=%s, abstract=%s WHERE id=%s;"  # SQLクエリを定義
            cur.execute(sql, (uid, newChatName, newChatDescription, cid))  # クエリを実行
            conn.commit()  # トランザクションをコミット
        except Exception as e:
            print(e + 'が発生しました')  # エラーメッセージを出力
            abort(500)  # HTTP 500エラーを返す
        finally:
            cur.close()  # カーソルを閉じる

    # チャットの削除
    def deleteChat(cid):
        try:
            conn = DB.getConnection()  # データベース接続を取得
            cur = conn.cursor()  # カーソルを作成
            sql = "DELETE FROM chat WHERE id=%s;"  # SQLクエリを定義
            cur.execute(sql, (cid,))  # クエリを実行
            conn.commit()  # トランザクションをコミット
        except Exception as e:
            print(e + 'が発生しています')  # エラーメッセージを出力
            abort(500)  # HTTP 500エラーを返す
        finally:
            cur.close()  # カーソルを閉じる