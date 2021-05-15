from flask import Flask, request
import os

import pymysql
import pymysql.cursors


app = Flask(__name__)

# Connect to the database
connection = pymysql.connect(host=os.environ.get('us-cdbr-east-03.cleardb.com'),
                             user=os.environ.get('bffbfcd0c09f06'),
                             password=os.environ.get('a3415195'),
                             db=os.environ.get('heroku_d6918b07f609b9c'),
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

with connection.cursor() as cursor:
    # Create a new record
    sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
    cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

connection.commit()


@app.route('/')
def hello():
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT `id`, `email` FROM `users` WHERE `email`=%s"
        cursor.execute(sql, ('webmaster@python.org',))
        result = cursor.fetchone()
        print(result)
    return f'Hello, Heroku {result["email"]}!'

if __name__ == 'main':

    app.run() #啟動伺服器