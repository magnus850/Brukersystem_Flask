from flask import Flask, jsonify
from flask_cors import CORS
import mariadb
import os
from dotenv import load_dotenv

load_dotenv()
conn = mariadb.connect(
    user = os.getenv('DB_BRUKER'),
    password= os.getenv('DB_PASSORD'),
    host = os.getenv('DB_HOST'),
    database = os.getenv('DB'),
    unix_socket = '/opt/homebrew/var/mysql/mysql.sock'
    )

cur = conn.cursor()

app = Flask(__name__)
CORS(app)
@app.route("/")
def forside():
    cur.execute("select * from brukere;")
    data = cur.fetchall()
    return jsonify({"brukere":data})

@app.route("/logginn")
def logg_inn_side():
    cur.execute()

if __name__ == "__main__":
    app.run(debug=True)