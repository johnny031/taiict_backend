from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from models import db, News, File
import shutil
import json
import os

delete_news = Blueprint("delete_news", __name__)

@delete_news.route('/json-data', methods=["GET","POST"])
@cross_origin()
def news_delete():
    if request.method == "POST":
        news = json.loads(request.data)
        newsId = news["newsId"]   
        files_del = File.query.filter_by(news_Id=newsId).all()
        for file_del in files_del:
            if file_del is not None:
                try:
                    shutil.rmtree(os.path.join('static/uploads/', str(file_del.id)))
                except:
                    pass
        news_del = News.query.filter_by(newsId=newsId).first()
        db.session.delete(news_del)
        db.session.commit()
        return jsonify({})
    else:
        news = News.query.all()
        list = [[i.newsId, i.author, i.datetime, i.title, i.content, 
        [[j.id, j.name] for j in i.files]] for i in news]
        return jsonify(list)