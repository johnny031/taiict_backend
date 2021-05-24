from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()
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
class File(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable=False)
    news_Id = db.Column(db.Integer, db.ForeignKey("news.newsId"), nullable=False)