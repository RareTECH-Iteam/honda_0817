from flask import Flask, request, redirect, render_template, session, flash, abort, jsonify
from datetime import timedelta
import hashlib
import uuid
import re
from flask_socketio import SocketIO, emit
import mysql.connector
from mysql.connector import Error
import os
from models import dbConnect


app = Flask(__name__)
app.secret_key = uuid.uuid4().hex
app.permanent_session_lifetime = timedelta(days=30)
# Socket.IO の設定
socketio = SocketIO(app)

# サインアップページの表示
@app.route('/signup')
def signup():
    return render_template('registration/signup.html')

# サインアップ処理
@app.route('/signup', methods=['POST'])
def userSignup():
    username = request.form.get('username')
    email = request.form.get('email')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')
    address = request.form.get('address')
    greeting = request.form.get('greeting')

    pattern = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    if username == '' or email =='' or password1 == '' or password2 == '' or address == '' or greeting == '':
        flash('空のフォームがあるようです')
    elif password1 != password2:
        flash('二つのパスワードの値が違っています')
    elif re.match(pattern, email) is None:
        flash('正しいメールアドレスの形式ではありません')
    else:
        uid = uuid.uuid4()
        # password = hashlib.sha256(password1.encode('utf-8')).hexdigest()
        password = password1  # ハッシュ化しない
        DBuser = dbConnect.getUser(email)

        if DBuser != None:
            flash('既に登録されているようです')
        else:
            dbConnect.createUser(uid, username, email, password, address, greeting)
            UserId = str(uid)
            session['uid'] = UserId
            return redirect('/')
    return redirect('/signup')

# ログインページの表示
@app.route('/login')
def login():
    return render_template('registration/login.html')

# ログイン処理
@app.route('/login', methods=['POST'])
def userLogin():
    email = request.form.get('email')
    password = request.form.get('password')

    if email =='' or password == '':
        flash('空のフォームがあるようです')
    else:
        user = dbConnect.getUser(email)
        if user is None:
            flash('このユーザーは存在しません')
        else:
            if password != user["password"]:  # ハッシュ化せずに平文で比較
                flash('パスワードが間違っています！')
            # hashPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
            # if hashPassword != user["password"]:
            #     flash('パスワードが間違っています！')
            else:
                session['uid'] = user["uid"]
                return redirect('/')
    return redirect('/login')

# 一覧ページの表示
@app.route('/')
def index():
    uid = session.get("uid")
    if uid is None:
        return redirect('/login')
    else:
        channels = dbConnect.getChatAll()
        channels = channels[::-1]  # スライスを使ってタプルを逆順にする
    return render_template('index.html', channels=channels, uid=uid)

# ホームの「/」の中の「detail」URLのエンドポイント
@app.route('/detail')
def detail():
    uid = session.get("uid")
    if uid is None:
        return redirect('/login')
    else:
        user = dbConnect.getUserByUid(uid)
    return render_template('detail.html', user=user)

# ユーザ情報の更新
@app.route('/detail_edit', methods=['GET', 'POST'])
def detail_edit():
    uid = session.get("uid")
    if uid is None:
        return redirect('/login')

    if request.method == 'POST':
        # POSTリクエストの場合、フォームからデータを取得して更新処理を行う
        username = request.form.get('username')
        email = request.form.get('email')
        address = request.form.get('address')
        greeting = request.form.get('greeting')

        # データベースを更新
        dbConnect.updateUser(uid, username, email, address, greeting)
        
        # 更新後の詳細ページにリダイレクト
        return redirect('/detail')
    else:
        # GETリクエストの場合、ユーザー情報を取得して編集ページを表示
        user = dbConnect.getUserByUid(uid)
        return render_template('detail_edit.html', user=user)

# ホームの「/」の中の「chat_room_list」URLのエンドポイント
@app.route('/chat_room_list')
def chat_room_list():
    uid = session.get("uid")
    if uid is None:
        return redirect('/login')
    chat_rooms = dbConnect.getChatRoomList(uid)
    return render_template('chat_room_list.html', chat_rooms=chat_rooms)

# chat_room.htmlのURLのエンドポイント
@app.route('/chat_room', methods=['GET', 'POST'])
def chat_room():
    uid = session.get("uid")
    if uid is None:
        return redirect('/login')
    
    chat_id = request.args.get('room_id')  # URL パラメータからチャットIDを取得
    if chat_id is None:
        return redirect('/chat_room_list')  # チャットIDが指定されていない場合はチャットルームリストにリダイレクト

    if request.method == 'POST':
        # メッセージの投稿
        message = request.form.get('message')
        
        if message:
            dbConnect.createMessage(uid, chat_id, message)
            # Socket.IO を利用してメッセージを全クライアントにブロードキャスト
            socketio.emit('new_message', {'uid': uid, 'chat_id': chat_id, 'message': message}, room=chat_id)
            return redirect(f'/chat_room?room_id={chat_id}')

    # メッセージの取得
    messages = dbConnect.getMessagesByChatRoom(uid, chat_id)
    return render_template('chat_room.html', chat_id=chat_id, messages=messages)

@socketio.on('chat message')
def handle_chat_message(data):
    uid = session.get("uid")
    chat_id = request.args.get('room_id')
    message = data.get('message')
    if uid and chat_id and message:
        try:
            dbConnect.createMessage(uid, chat_id, message)
            # クライアントに新しいメッセージをブロードキャスト
            socketio.emit('chat message', {'uid': uid, 'chat_id': chat_id, 'message': message}, broadcast=True)
        except Exception as e:
            print(f'Error: {str(e)}')

# チャットルームの表示とメッセージ送信のエンドポイント
# @app.route('/chat_room', methods=['GET', 'POST'])
# def chat_room():
#     uid = session.get("uid")
#     if uid is None:
#         return redirect('/login')
    
#     if request.method == 'POST':
#         data = request.get_json()
#         chat_id = data.get('chat_id')
#         message = data.get('message')
        
#         if chat_id and message:
#             if chat_id.isdigit():  # chat_id が数字かどうかを確認
#                 dbConnect.addMessage(uid, int(chat_id), message)
#                 return jsonify(success=True)
#             else:
#                 return jsonify(success=False, error="Invalid chat_id")
#         else:
#             return jsonify(success=False, error="Invalid data")
    
#     # GETリクエストの場合、チャットルームを表示
#     chat_id = request.args.get('chat_id')
    
#     if chat_id:
#         if chat_id.isdigit():  # chat_id が数字かどうかを確認
#             messages = dbConnect.getMessagesByChatRoom(uid, int(chat_id))
#             return jsonify(success=True, messages=messages)
#         else:
#             return jsonify(success=False, error="Invalid chat_id")
    
#     # チャットIDが指定されていない場合、チャットルームの一覧を表示
#     chats = dbConnect.getChatRoomList(uid)
#     return render_template('chat_room.html', chats=chats, chat_id=chat_id)


    
    # チャットIDが指定されていない場合、チャットルームの一覧を表示
    chats = dbConnect.getChatRoomList(uid)
    return render_template('chat_room.html', chats=chats)

# @app.route('/fetch_messages')
# def fetch_messages():
#     chat_id = request.args.get('chat_id')
#     uid = session.get("uid")
#     if uid is None:
#         return redirect('/login')
    
#     if chat_id and chat_id.isdigit():
#         messages = dbConnect.getMessagesByChatRoom(uid, int(chat_id))
#         return jsonify(success=True, messages=messages)
#     else:
#         return jsonify(success=False, error="Invalid chat_id")

@app.route('/fetch_messages')
def fetch_messages():
    chat_id = request.args.get('chat_id')
    if chat_id:
        messages = dbConnect.getMessagesByChatRoom(chat_id)
        return jsonify({'success': True, 'messages': messages})
    else:
        return jsonify({'success': False, 'error': 'チャットIDが指定されていません'})

# 「matching」URLのエンドポイント
@app.route('/matching')
def matching():
    return render_template('matching.html')


# 「matching_confirm」URLのエンドポイント
@app.route('/matching_confirm')
def matching_confirm():
    return render_template('matching_confirm.html')

# マッチングリクエスト一覧ページの表示
@app.route('/request_list.html')
def matching_request_list():
    return render_template('request_list.html')

@app.route('/logout')
def logout():
    return render_template('registration/login.html')

# Socket.IO のイベントハンドラー
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

# Socket.IO のエラーハンドリング
@socketio.on_error()
def handle_error(e):
    print(f'Error: {e}')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)

