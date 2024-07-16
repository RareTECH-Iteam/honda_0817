import pymysql
from util.DB import DB

class dbConnect:
    # ユーザー情報の追加
    def createUser(uid, name, email, password):
        try:
            conn = DB.getConnection()  # データベース接続を取得
            cur = conn.cursor()  # カーソルを作成
            sql = "INSERT INTO users (uid, user_name, email, password) VALUES (%s, %s, %s, %s);"  # SQLクエリを定義
            cur.execute(sql, (uid, name, email, password))  # クエリを実行
            conn.commit()  # トランザクションをコミット
        except Exception as e:
            print(e + 'が発生しています')  # エラーメッセージを出力
            abort(500)  # HTTP 500エラーを返す
        finally:
            cur.close()  # カーソルを閉じる