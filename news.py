from flask import Blueprint, render_template
from flask_login import current_user, login_required
from models import News

news = Blueprint("news", __name__, static_folder="static", template_folder="templates")

@news.route('/news-list', methods=["GET"])
@login_required
def news_list():
    news = News.query.all()
    return render_template("news.html", news=news, username=current_user.name, is_premium=current_user.premium)