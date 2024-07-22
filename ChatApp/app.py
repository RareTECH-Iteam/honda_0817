from flask import Flask, request, redirect, render_template, session, flash, abort
from datetime import timedelta
import hashlib
import uuid
import re

from models import dbConnect

app = Flask(__name__)
app.secret_key = uuid.uuid4().hex
app.permanent_session_lifetime = timedelta(days=30)


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
        password = hashlib.sha256(password1.encode('utf-8')).hexdigest()
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
            hashPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
            if hashPassword != user["password"]:
                flash('パスワードが間違っています！')
            else:
                session['uid'] = user["uid"]
                return redirect('/')
    return redirect('/login')

# チャンネル一覧ページの表示
@app.route('/')
def index():
    uid = session.get("uid")
    if uid is None:
        return redirect('/login')
    else:
        channels = dbConnect.getChatAll()
        channels.reverse()
    return render_template('index.html', channels=channels, uid=uid)



# ホームの「/」の中の「detail」URLのエンドポイント
@app.route('/detail')
def detail():
    return render_template('detail.html')

@app.route('/detail_edit')
def detail_edit():
    return render_template('detail_edit.html')

# ホームの「/」の中の「chat_room_list」URLのエンドポイント
@app.route('/chat_room_list')
def chat_room_list():
    return render_template('chat_room_list.html')

@app.route('/chat_room')
def chat_room():
    return render_template('chat_room.html')


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



if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)

