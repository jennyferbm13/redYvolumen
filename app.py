import time
import mysql.connector
from flask import Flask

app = Flask(__name__)
def getDB():
  attempts=0
  while True:
    try:
      return mysql.connector.connect(host="mysql", user ="root", password="goku",database="mydatabase")
    except mysql.connector.Error as err:
     attempts +=1
     print(err)
     print("Error Code: ", err.errno)
     print("SQLSTATE ", err.sqlstate)
     print("Message: ", err.msg)
     print("Attempt: ", attempts)
     time.sleep(0.5)
db = getDB()
cache=db.cursor()
cache.execute("SHOW DATABASES")
rows=cache.fetchall()
cache.execute("CREATE TABLE IF NOT EXISTS info (data VARCHAR(255) NOT NULL, value INT,UNIQUE (data))")
SQL= "INSERT IGNORE INTO info (data,value) VALUES ('hits',0)"

try:
    cache.execute(SQL)
    db.commit()
    cache.execute("SELECT value FROM info WHERE data = 'hits'")
    hits= cache.fetchone()[0]
except mysql.connector.Error as err:
     print(err)
     print("Error Code: ", err.errno)
     print("SQLSTATE ", err.sqlstate)
     print("Message: ", err.msg)
    
def get_hit_count():
   retries = 5
   try:
      cache.execute("UPDATE info SET value = value+1")
      db.commit()
      cache.execute("SELECT value FROM info WHERE data = 'hits'")
      hits = cache.fetchone()[0]
      return hits
   except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.msg)
            print("Message: ", err.msg)
            return -1


@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)

