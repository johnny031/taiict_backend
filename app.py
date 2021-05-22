from flask import Flask, request, render_template, jsonify, url_for, redirect, flash, session
from flask_cors import cross_origin
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, func
from datetime import datetime, timezone, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import dj_database_url
import json
import os

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

app.config["SECRET_KEY"] = "Thisismysecretkeyandsupposenottobeknownfromothers"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024 # 1 MB

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://hYVZeathwy:8XlyxUFPDf@remotemysql.com/hYVZeathwy"

# heroku connect database
DATABASES = {
    'default': 'mysql://hYVZeathwy:8XlyxUFPDf@remotemysql.com/hYVZeathwy'
}
DATABASES['default'] = dj_database_url.config(
    default='mysql://hYVZeathwy:8XlyxUFPDf@remotemysql.com/hYVZeathwy',
)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "您沒有權限，請先登入"
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    premium = db.Column(db.Boolean(), nullable=False)

class News(db.Model):
    newsId = db.Column(db.Integer, primary_key = True)
    author = db.Column(db.String(50), nullable=False)
    datetime = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(3000), nullable=False)
    files = db.relationship("File", cascade="all,delete", backref="news")

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
class File(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable=False)
    news_Id = db.Column(db.Integer, db.ForeignKey("news.newsId"), nullable=False)

# News.__table__.drop(db.engine)
# new_news = News(author="author", title="title", content="content")
# db.session.add(new_news)
# News.query.filter(News.newsId == 249).delete()
# db.session.commit()

# news_del = News.query.filter_by(newsId=274).first()
# db.session.delete(news_del)
# db.session.commit()

# news = News.query.all()
# print(news)


@login_manager.user_loader
def load_user(id):
    user = User.query.get(id)
    return user

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
            user = User.query.filter_by(name=func.binary(name)).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('news_list'))
            else:
                flash('使用者名稱或密碼輸入錯誤')
                return redirect(url_for('login'))
    return render_template("index.html")

@app.route('/news-list', methods=["GET"])
@login_required
def news_list():
    news = News.query.all()
    return render_template("news.html", news=news, username=current_user.name)

@app.route('/add-news', methods=["POST", "GET"])
@login_required
def add_news():
    if request.method == "POST":
        author = request.form["author"]
        title = request.form["title"]
        content = request.form["content"]
        
        tz = timezone(timedelta(hours=+8))
        datetime_str = datetime.now(tz).strftime("%Y/%m/%d %H:%M:%S")
        session["datetime_str"] = datetime_str
        new_news = News(author=author, datetime=datetime_str, title=title, content=content)
        db.session.add(new_news)
        db.session.commit()

        if 'file' not in request.files:
            return jsonify({}) 
        files = request.files.getlist("file")
        print(files)
        
        for file in files:
            if file.filename == '':
                return jsonify({})
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                if len(filename) < 5:
                    filename = "." + filename
                file_obj = File(name=filename, news=new_news)
                db.session.add(file_obj)
                db.session.commit()
                new_file = db.session.query(File).order_by(File.id.desc()).first()
                _id = str(new_file.id)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], _id + "_" + filename))
        return jsonify({})  
    else:
        news_added = News.query.filter_by(datetime=session["datetime_str"]).first()
        session.pop("datetime_str")
        return jsonify(news_added.newsId, news_added.datetime)

@app.route('/json-data', methods=["GET","POST"])
@cross_origin()
def delete_note():
    if request.method == "POST":
        news = json.loads(request.data)
        newsId = news["newsId"]   
        files_del = File.query.filter_by(news_Id=newsId).all()
        for file_del in files_del:
            if file_del is not None:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], str(file_del.id) + "_" + file_del.name))

        news_del = News.query.filter_by(newsId=newsId).first()
        db.session.delete(news_del)
        db.session.commit()
        return jsonify({})
    else:
        news = News.query.all()
        list = [[i.newsId, i.author, i.datetime, i.title, i.content, 
        [[j.id, j.name] for j in i.files]] for i in news]
        return jsonify(list)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/<filename>')
def display_image(filename):
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == 'main':
    db.create_all()
    app.run()