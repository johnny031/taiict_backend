import mysql.connector
from flask import Flask, request, render_template, jsonify, url_for, redirect, flash, session
from flask_cors import cross_origin
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user
from datetime import datetime, timezone, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import json

app = Flask(__name__)

app.config["SECRET_KEY"] = "Thisismysecretkeyandsupposenottobeknownfromothers"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "您沒有權限，請先登入"
class User(UserMixin):
    def __init__(self, name, password):
        self.name = name
        self.password = password

    @property
    def id(self):
        return self.name

@login_manager.user_loader
def load_user(name):
    user = User(name=name, password="")
    return user

def get_data(cursor):
    list = []
    for x in cursor:
        list.append(x)
    return list  
# db = mysql.connector.connect(
#     host = "remotemysql.com",
#     user = "hYVZeathwy",
#     passwd = "8XlyxUFPDf",
#     database = "hYVZeathwy"
# )
# cursor = db.cursor()
# cursor.execute("DELETE FROM User")
# cursor.execute("CREATE TABLE News (newsID int PRIMARY KEY AUTO_INCREMENT, author VARCHAR(50) NOT NULL, datetime VARCHAR(50) NOT NULL, title VARCHAR(80) NOT NULL, content VARCHAR(3000) NOT NULL)")
# cursor.execute("CREATE TABLE User (userID int PRIMARY KEY AUTO_INCREMENT, name VARCHAR(50) NOT NULL, password VARCHAR(80) NOT NULL)")
# cursor.execute("INSERT INTO News (author, datetime, title, content) VALUES (%s, %s, %s, %s)", ("John", datetime.now(), "First news title", "First news content"))
# hashed = generate_password_hash("secrettaiict", method="sha256")
# cursor.execute("INSERT INTO User (name, password) VALUES (%s, %s)", ("John", "test"))
# db.commit() 
# cursor.execute("SELECT * FROM User")
# list = []
# for x in cursor:
#     list.append(x)
# print(list)
# cursor.close()
# db.close()
@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(hours=1)

@app.route('/', methods=['GET', 'POST'])  
def login(): 
    if request.method == "POST":
        name = request.form.get('name')
        password = request.form.get('password')
        if len(name)>0 and len(password)>0:
            db = mysql.connector.connect(
                host = "remotemysql.com",
                user = "hYVZeathwy",
                passwd = "8XlyxUFPDf",
                database = "hYVZeathwy"
            )
            cursor = db.cursor()
            cursor.execute(f"SELECT password FROM User WHERE BINARY name = '{name}'")
            list = get_data(cursor)
            cursor.close()
            db.close()
            if len(list)>0 and check_password_hash(list[0][0], password):
                user = User(name=name, password=password)
                login_user(user)
                return redirect(url_for('news_list'))
            else:
                flash('使用者名稱或密碼輸入錯誤')
                return redirect(url_for('login'))
    return render_template("index.html")

@app.route('/news-list', methods=["GET"])
@login_required
def news_list():
    db = mysql.connector.connect(
        host = "remotemysql.com",
        user = "hYVZeathwy",
        passwd = "8XlyxUFPDf",
        database = "hYVZeathwy"
    )
    cursor = db.cursor()
    cursor.execute("SELECT * FROM News")
    list = get_data(cursor)
    cursor.close()
    db.close()
    return render_template("news.html", list=list, username=current_user.name)

@app.route('/add-news', methods=["POST", "GET"])
@login_required
def add_news():
    db = mysql.connector.connect(
        host = "remotemysql.com",
        user = "hYVZeathwy",
        passwd = "8XlyxUFPDf",
        database = "hYVZeathwy"
    )
    cursor = db.cursor()
    if request.method == "POST":
        data = json.loads(request.data)
        author = data["author"]
        title = data["title"]
        content = data["content"]
        tz = timezone(timedelta(hours=+8))
        datetime_str = datetime.now(tz).strftime("%Y/%m/%d %H:%M:%S")
        session["datetime_str"] = datetime_str
        cursor.execute("INSERT INTO News (author, datetime, title, content) VALUES (%s, %s, %s, %s)", (author, datetime_str, title, content))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({})  
    else:
        cursor.execute(f"SELECT newsId, datetime FROM News WHERE datetime = '{session['datetime_str']}'")
        list = get_data(cursor)
        cursor.close()
        db.close()
        session.pop('datetime_str')
        return jsonify(list)

@app.route('/json-data', methods=["GET","POST"])
@cross_origin()
def delete_note():
    db = mysql.connector.connect(
        host = "remotemysql.com",
        user = "hYVZeathwy",
        passwd = "8XlyxUFPDf",
        database = "hYVZeathwy"
    )
    cursor = db.cursor()
    if request.method == "POST":
        news = json.loads(request.data)
        newsId = news["newsId"]
        cursor.execute(f"DELETE FROM News WHERE newsId = {newsId}")
        db.commit()
        cursor.close()
        db.close()
        return jsonify({})
    else:
        cursor.execute("SELECT * FROM News")
        list = get_data(cursor)
        cursor.close()
        db.close()
        return jsonify(list)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == 'main':
    app.run()