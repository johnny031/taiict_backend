from flask import Blueprint, request, jsonify, session
from flask_login import login_required
from werkzeug.utils import secure_filename
from models import db, File
import os

upload = Blueprint("upload", __name__)

@upload.route("/upload", methods=['POST', 'GET'])
@login_required
def upload_file():
    if request.method == "POST":
        if 'file' not in request.files:
            return jsonify({}) 
        files = request.files.getlist("file")
        session["files_id"] = []
        for file in files:
            if file.filename == '':
                continue
            filename = secure_filename(file.filename)
            if "." not in filename:
                filename = "." + filename
            file_obj = File(name=filename)
            db.session.add(file_obj)
            db.session.commit()
            new_file = db.session.query(File).order_by(File.id.desc()).first()
            _id = str(new_file.id)
            session["files_id"].append(_id)
            file.save(os.path.join('static/uploads/', _id + "_" + filename))
        return jsonify({})  
    else:    
        file_id = session["files_id"]
        filenames = []
        for i in file_id:
            item = File.query.filter_by(id=i).first()
            filenames.append(item.name)
        session.pop("files_id")
        return jsonify(file_id, filenames)