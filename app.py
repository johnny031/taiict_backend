import mysql.connector
from flask import Flask, request

app = Flask(__name__)


db = mysql.connector.connect(
    host = "us-cdbr-east-03.cleardb.com",
    user = "bffbfcd0c09f06",
    passwd = "a3415195",
    database = "heroku_d6918b07f609b9c"
)

cursor = db.cursor()

# cursor.execute("CREATE TABLE Person (name VARCHAR(50), age smallint UNSIGNED, persionID int PRIMARY KEY AUTO_INCREMENT)")

# cursor.execute("INSERT INTO Person (name, age) VALUES (%s, %s)", ("John", 23))
# db.commit()

cursor.execute("SELECT * FROM Person")

for x in cursor:
    print(x)

@app.route('/')
def hello():
    for x in cursor:
        return f'Hello, Heroku! {x}'

if __name__ == 'main':
    app.run()