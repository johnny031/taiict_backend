import mysql.connector
from flask import Flask, request, render_template, jsonify
from flask_cors import cross_origin
from datetime import datetime, timezone, timedelta
import json

app = Flask(__name__)

# cursor.execute("DROP TABLE News")
# cursor.execute("CREATE TABLE News (newsID int PRIMARY KEY AUTO_INCREMENT, author VARCHAR(50) NOT NULL, datetime VARCHAR(50) NOT NULL, title VARCHAR(80) NOT NULL, content VARCHAR(3000) NOT NULL)")
# cursor.execute("INSERT INTO News (author, datetime, title, content) VALUES (%s, %s, %s, %s)", ("John", datetime.now(), "First news title", "First news content"))
# db.commit()

# cursor.execute("SELECT * FROM News")

# list = []
# for x in cursor:
#     list.append(x)
# print(list)

@app.route('/', methods=["GET", "POST"])
def hello():
    db = mysql.connector.connect(
        # heroku cleardb database
        # host = "us-cdbr-east-03.cleardb.com",
        # user = "bffbfcd0c09f06",
        # passwd = "a3415195",
        # database = "heroku_d6918b07f609b9c"

        # remote mysql database
        host = "remotemysql.com",
        user = "hYVZeathwy",
        passwd = "8XlyxUFPDf",
        database = "hYVZeathwy"
    )
    cursor = db.cursor()
    if request.method == "POST":
        author = request.form.get("author")
        title = request.form.get("title")
        content = request.form.get("content")
        if len(author) > 0 and len(title) > 0 and len(content) > 0:
            tz = timezone(timedelta(hours=+8))
            datetime_str = datetime.now(tz).strftime("%Y/%m/%d %H:%M:%S")
            cursor.execute("INSERT INTO News (author, datetime, title, content) VALUES (%s, %s, %s, %s)", (author, datetime_str, title, content))
            db.commit()
            
    cursor.execute("SELECT * FROM News")
    list = []
    for x in cursor:
        list.append(x)
    print(list) 
    cursor.close()
    db.close()
    return render_template("index.html", list=list)

@app.route('/json-data', methods=["GET","POST"])
@cross_origin()
def delete_note():
    db = mysql.connector.connect(
        host = "remotemysql.com",
        user = "hYVZeathwy",
        passwd = "8XlyxUFPDf",
        database = "hYVZeathwy"
    )
    cursor = db.cursor()
    if request.method == "POST":
        news = json.loads(request.data)
        newsId = news["newsId"]
        cursor.execute(f"DELETE FROM News WHERE newsId = {newsId}")
        db.commit()
        cursor.close()
        db.close()
        return jsonify({})
    else:
        cursor.execute("SELECT * FROM News")
        list = []
        for x in cursor:
            list.append(x)
        cursor.close()
        db.close()
        return jsonify(list)
    

if __name__ == 'main':
    app.run()