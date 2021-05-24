from flask import Blueprint, render_template, request, url_for, redirect, flash
from models import User
from sqlalchemy import func
from werkzeug.security import check_password_hash
from flask_login import login_user

login = Blueprint("login", __name__, static_folder="static", template_folder="templates")

@login.route("/", methods=['GET', 'POST'])
def user_login(): 
    if request.method == "POST":
        name = request.form.get('name')
        password = request.form.get('password')
        if len(name)>0 and len(password)>0:
            user = User.query.filter_by(name=func.binary(name)).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('news.news_list'))
            else:
                flash('使用者名稱或密碼輸入錯誤')
                return redirect(url_for('login.user_login'))
    return render_template("index.html")