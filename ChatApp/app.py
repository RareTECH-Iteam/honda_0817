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
    name = request.form.get('name')
    email = request.form.get('email')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    pattern = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    if name == '' or email =='' or password1 == '' or password2 == '':
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
            dbConnect.createUser(uid, name, email, password)
            UserId = str(uid)
            session['uid'] = UserId
            return redirect('/')
    return redirect('/signup')


# ログインページの表示
@app.route('/login')
def login():
    return render_template('registration/login.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)