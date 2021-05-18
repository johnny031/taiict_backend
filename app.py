import mysql.connector
from flask import Flask, request, render_template, jsonify, url_for, redirect, flash
from flask_cors import cross_origin
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user
from datetime import datetime, timezone, timedelta
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
        self.hash = password

    @property
    def id(self):
        return self.name

@login_manager.user_loader
def load_user(name):
    return User

# db = mysql.connector.connect(
#     host = "remotemysql.com",
#     user = "hYVZeathwy",
#     passwd = "8XlyxUFPDf",
#     database = "hYVZeathwy"
# )
# cursor = db.cursor()
# cursor.execute("DROP TABLE User")
# cursor.execute("CREATE TABLE News (newsID int PRIMARY KEY AUTO_INCREMENT, author VARCHAR(50) NOT NULL, datetime VARCHAR(50) NOT NULL, title VARCHAR(80) NOT NULL, content VARCHAR(3000) NOT NULL)")
# cursor.execute("CREATE TABLE User (userID int PRIMARY KEY AUTO_INCREMENT, name VARCHAR(50) NOT NULL, password VARCHAR(80) NOT NULL)")
# cursor.execute("INSERT INTO News (author, datetime, title, content) VALUES (%s, %s, %s, %s)", ("John", datetime.now(), "First news title", "First news content"))
# cursor.execute("INSERT INTO User (name, password) VALUES (%s, %s)", ("John", "taiictpassword"))
# db.commit()

# cursor.execute("SELECT * FROM User")
# list = []
# for x in cursor:
#     list.append(x)
# print(list)
# cursor.close()
# db.close()
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
            cursor.execute(f"SELECT password FROM User WHERE name = '{name}'")
            list = []
            for x in cursor:
                list.append(x)
            cursor.close()
            db.close()
            if len(list)>0 and list[0][0] == password:
                user = User(name=name, password=password)
                login_user(user)
                return redirect(url_for('news_list'))
            else:
                flash('使用者名稱或密碼輸入錯誤')
                return redirect(url_for('login'))
    return render_template("index.html")

@app.route('/news-list', methods=["GET", "POST"])
@login_required
def news_list():
    db = mysql.connector.connect(
        host = "remotemysql.com",
        user = "hYVZeathwy",
        passwd = "8XlyxUFPDf",
        database = "hYVZeathwy"
    )
    cursor = db.cursor()
    if request.method == "POST":
        author = request.form.get("author")
        title = request.form.get("title")
        content = request.form.get("content")
        if len(author) > 0 and len(title) > 0 and len(content) > 0:
            tz = timezone(timedelta(hours=+8))
            datetime_str = datetime.now(tz).strftime("%Y/%m/%d %H:%M:%S")
            cursor.execute("INSERT INTO News (author, datetime, title, content) VALUES (%s, %s, %s, %s)", (author, datetime_str, title, content))
            db.commit()
    cursor.execute("SELECT * FROM News")
    list = []
    for x in cursor:
        list.append(x)
    cursor.close()
    db.close()
    return render_template("news.html", list=list)

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
        list = []
        for x in cursor:
            list.append(x)
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