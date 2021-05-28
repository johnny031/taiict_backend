from flask import Blueprint, render_template
from flask_login import current_user, login_required
from models import db, News, File
import shutil
import os

news = Blueprint("news", __name__)

@news.route('/news-list', methods=["GET"])
@login_required
def news_list():
    news = News.query.all()
    files_del = File.query.filter_by(news_Id=None).all()
    if len(files_del) > 0:
        for file_del in files_del:
            if file_del is not None:
                try:
                    shutil.rmtree(os.path.join('static/uploads/', str(file_del.id)))
                except:
                    pass
        File.query.filter(File.news_Id == None).delete(synchronize_session=False)
        db.session.commit()
    return render_template("news.html", news=news, username=current_user.name, is_premium=current_user.premium)