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

    # すべてのチャンネルを取得
    def getChannelAll():
        try:
            conn = DB.getConnection()  # データベース接続を取得
            cur = conn.cursor()  # カーソルを作成
            sql = "SELECT * FROM channels;"  # SQLクエリを定義
            cur.execute(sql)  # クエリを実行
            channels = cur.fetchall()  # 結果を全て取得
            return channels  # チャンネル情報を返す
        except Exception as e:
            print(e + 'が発生しています')  # エラーメッセージを出力
            abort(500)  # HTTP 500エラーを返す
        finally:
            cur.close()  # カーソルを閉じる