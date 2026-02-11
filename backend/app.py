from flask import Flask, jsonify, request
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

def brukernavn_sjekk(brukernavn, passord):
    cur.execute(
        'SELECT id, passord FROM brukere WHERE bruker =%s AND passord = %s',
        (brukernavn, passord))
    resultat = cur.fetchone()
    print(resultat)
    if resultat == None:
        return 'Feil brukernavn og/eller passord' 
    else: return 'Riktig brukernavn og passord'
    
def registrer_bruker(brukernavn, passord):
    cur.execute('select bruker from brukere where bruker = %s',
            (brukernavn,))
    if cur.fetchone() != None:
        return 'Brukernavn er tatt, velg et annet'
    elif cur.fetchone() == None: 
        cur.execute(
        'insert into brukere (bruker, passord) values (%s, %s)',
        (brukernavn, passord))
        conn.commit()
        return f"Du har lagd en ny bruker kalt: {brukernavn}"

    
#routes
@app.route("/")
def forside():
    cur.execute("select * from brukere;")
    data = cur.fetchall()
    return jsonify({"brukere":data})

@app.route("/inputdata", methods=['POST'])
def logg_inn_side():
    data = request.json
    brukernavn = (data.get('brukernavn'))
    passord = (data.get('passord'))
    melding = brukernavn_sjekk(brukernavn, passord)
    return melding
    
@app.route("/regdata", methods=['POST'])
def registrerings_side():
    data = request.json
    brukernavn = (data.get('brukernavn'))
    passord = (data.get('passord'))
    melding = registrer_bruker(brukernavn, passord)
    return melding

if __name__ == "__main__":
    app.run(debug=True)
    
