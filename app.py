import mysql.connector
from flask import Flask, request, render_template, jsonify
import json

app = Flask(__name__)


db = mysql.connector.connect(
    host = "us-cdbr-east-03.cleardb.com",
    user = "bffbfcd0c09f06",
    passwd = "a3415195",
    database = "heroku_d6918b07f609b9c"
)
 
cursor = db.cursor()

# cursor.execute("DROP TABLE Note")
# cursor.execute("CREATE TABLE Note (note VARCHAR(50),name VARCHAR(50), noteID int PRIMARY KEY AUTO_INCREMENT)")
# cursor.execute("INSERT INTO Note (note, name) VALUES (%s, %s)", ("First note", "John"))
# cursor.execute("INSERT INTO Note (note, name) VALUES (%s, %s)", ("Second note", "Joe"))
# cursor.execute("INSERT INTO Note (note, name) VALUES (%s, %s)", ("Third note", "Mary"))
# db.commit()

# cursor.execute("SELECT * FROM Note")

# list = []
# for x in cursor:
#     list.append(x)
# print(list)


@app.route('/', methods=["GET", "POST"])
def hello():
    if request.method == "POST":
        note = request.form.get("note")
        if len(note) > 0:
            cursor.execute("INSERT INTO Note (note, name) VALUES (%s, %s)", (note, "John"))
            db.commit()
            
    cursor.execute("SELECT * FROM Note")
    list = []
    for x in cursor:
        list.append(x)
    # print(list) 
    return render_template("index.html", list=list)

@app.route('/delete-note', methods=["POST"])
def delete_note():
    note = json.loads(request.data)
    noteId = note["noteId"]
    
    cursor.execute(f"DELETE FROM Note WHERE noteId = {noteId}")
    db.commit()
    return jsonify({})

if __name__ == 'main':
    app.run()