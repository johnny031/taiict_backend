# import mysql.connector
from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def hello():
    return f'Hello, Heroku!'

if __name__ == 'main':
    app.run()

    
# db = mysql.connector.connect(
#     host = "localhost",
#     user = "Johnny",
#     passwd = "Johnny123",
#     database = "testdatabase"
# )

# cursor = db.cursor()

# # cursor.execute("CREATE TABLE Person (name VARCHAR(50), age smallint UNSIGNED, persionID int PRIMARY KEY AUTO_INCREMENT)")

# # cursor.execute("INSERT INTO Person (name, age) VALUES (%s, %s)", ("Joe", 23))
# # db.commit()

# cursor.execute("SELECT * FROM Person")

# for x in cursor:
#     print(x)