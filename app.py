from flask import Flask, url_for, redirect, session, send_from_directory
from flask_login import LoginManager, login_required, logout_user
from datetime import timedelta
import dj_database_url
from models import db, User
from views.login import login
from views.news import news
from views.add_news import add_news
from views.delete_news import delete_news
from views.upload import upload
from views.delete_file import delete_file
import os

SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")

# from werkzeug.security import generate_password_hash
app = Flask(__name__)
app.register_blueprint(login)
app.register_blueprint(news)
app.register_blueprint(add_news)
app.register_blueprint(delete_news)
app.register_blueprint(upload)
app.register_blueprint(delete_file)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_RECYCLE'] = 1

## local production settings
# app.config['SECRET_KEY'] = "SECRET_KEY"
# app.config['SQLALCHEMY_DATABASE_URI'] = "DATABASE_URI"

# heroku connect database settings
DATABASES = {
    'default': DATABASE_URI
}
DATABASES['default'] = dj_database_url.config(
    default=DATABASE_URI,
)

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login.user_login"
login_manager.login_message = "您沒有權限，請先登入"

@login_manager.user_loader
def load_user(id):
    user = User.query.get(id)
    return user

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(hours=1)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login.user_login'))

@app.route('/download/<file_id>')
def download(file_id):
    path = os.path.join("static/uploads/", file_id)
    dirs = os.listdir(path)
    return send_from_directory(path, dirs[0], as_attachment=True)

if __name__ == 'main':
    db.create_all()
    app.run()