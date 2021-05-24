from flask import Blueprint, request, session, jsonify
from flask_login import login_required
from datetime import datetime, timezone, timedelta
from werkzeug.utils import secure_filename
from models import db, News, File
import os

add_news = Blueprint("add", __name__, static_folder="static", template_folder="templates")

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
        edit = request.form["edit"]   
        tz = timezone(timedelta(hours=+8))
        datetime_str = datetime.now(tz).strftime("%Y/%m/%d %H:%M:%S")
        session["datetime_str"] = datetime_str      
        if not len(edit) > 0:
            new_news = News(author=author, datetime=datetime_str, title=title, content=content)
            db.session.add(new_news)  
        else:
            News.query.filter(News.newsId == edit).update({"author":author, "datetime":datetime_str, "title":title, "content":content})
        db.session.commit()
        if 'file' not in request.files:
            return jsonify({}) 
        files = request.files.getlist("file")
        if len(edit) > 0:
            files_del = File.query.filter_by(news_Id=edit).all()
            for file_del in files_del:
                if file_del is not None:
                    os.remove(os.path.join('static/uploads/', str(file_del.id) + "_" + file_del.name))            
                db.session.delete(file_del)
                db.session.commit()
        for file in files:
            if file.filename == '':
                continue
            if not file or not allowed_file(file.filename):
                continue
            filename = secure_filename(file.filename)
            if len(filename) < 4:
                filename = "." + filename
            if len(edit) > 0:
                file_obj = File(name=filename, news_Id=edit)
            else:
                file_obj = File(name=filename, news=new_news)
            db.session.add(file_obj)
            db.session.commit()
            new_file = db.session.query(File).order_by(File.id.desc()).first()
            _id = str(new_file.id)
            file.save(os.path.join('static/uploads/', _id + "_" + filename))
        return jsonify({})  
    else:  
        news_added = News.query.filter_by(datetime=session["datetime_str"]).first()
        session.pop("datetime_str")
        return jsonify(news_added.newsId, news_added.datetime)