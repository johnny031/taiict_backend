from flask import Blueprint, request, jsonify
from flask_login import login_required
from models import db, File
import os

delete_file = Blueprint("delete_file", __name__)

@delete_file.route("/delete-file", methods=['POST'])
@login_required
def file_delete():  
    try:
        news_Id = request.form["edit"]
        files = File.query.filter_by(news_Id=news_Id).all()
        list = [[i.id, i.name] for i in files]
        return jsonify(list)
    except:
        file_id = request.form["file_id"]
        file_del = File.query.filter_by(id=file_id).first()
        try:
            os.remove(os.path.join('static/uploads/', str(file_del.id) + "_" + file_del.name))
        except:
            pass
        File.query.filter(File.id == file_id).delete(synchronize_session=False)
        db.session.commit()
        return jsonify({})