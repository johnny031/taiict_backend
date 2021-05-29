from flask import Blueprint, request, jsonify, session
from flask_login import login_required
from werkzeug.utils import secure_filename
from models import db, File
import os

upload = Blueprint("upload", __name__)

@upload.route("/upload", methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({}) 
    files = request.files.getlist("file")
    files_id = []
    for file in files:
        if file.filename == '':
            continue
        filename = file.filename
        file_obj = File(name=filename)
        db.session.add(file_obj)
        db.session.commit()
        new_file = db.session.query(File).order_by(File.id.desc()).first()
        _id = str(new_file.id)
        files_id.append(_id)
        path = os.path.join("static/uploads/", _id)
        os.makedirs(path)
        file.save(os.path.join(path, filename))
    return jsonify(files_id)  