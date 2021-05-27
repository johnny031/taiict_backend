from flask import Blueprint, request, session, jsonify
from flask_login import login_required
from datetime import datetime, timezone, timedelta
from werkzeug.utils import secure_filename
from models import db, News, File
import os

add_news = Blueprint("add", __name__)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'pdf', 'docx', 'doc', 'xlsx', 'pptx', 'ppt'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@add_news.route('/add-news', methods=["POST", "GET"])
@login_required
def news_add():
    if request.method == "POST":
        author = request.form["author"]
        title = request.form["title"]
        content = request.form["content"]
        file_id = request.form.getlist("file_id")

        edit = request.form["edit"]   
        tz = timezone(timedelta(hours=+8))
        datetime_str = datetime.now(tz).strftime("%Y/%m/%d %H:%M:%S")
        session["datetime_str"] = datetime_str      
        if not len(edit) > 0:
            new_news = News(author=author, datetime=datetime_str, title=title, content=content)
            db.session.add(new_news) 
            db.session.commit()
            for i in file_id:
                file_add = File.query.filter_by(id=i).first()
                file_add.news = new_news
        else:
            News.query.filter(News.newsId == edit).update({"author":author, "datetime":datetime_str, "title":title, "content":content})
            for i in file_id:
                File.query.filter(File.id == i).update({"news_Id":edit})
        db.session.commit()
        return jsonify({})
    else:  
        news_added = News.query.filter_by(datetime=session["datetime_str"]).first()
        session.pop("datetime_str")
        return jsonify(news_added.newsId, news_added.datetime)