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

def bruker_sjekk(brukernavn, passord):
    cur.execute(
        'SELECT id, passord, tillatelse FROM brukere WHERE bruker =%s AND passord = %s',
        (brukernavn, passord))
    resultat = cur.fetchone()
    if resultat == None:
        suksess = False
        return suksess, None 
    elif resultat: 
        resultat_liste = list(resultat)
        tillatelse = resultat_liste[2]
        suksess = True
        return suksess, tillatelse
    
    
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

#innlogging
@app.route("/inputdata", methods=['POST'])
def logg_inn_side():
    data = request.json
    brukernavn = (data.get('brukernavn'))
    passord = (data.get('passord'))
    suksess, tillatelse = bruker_sjekk(brukernavn, passord)
    print(suksess, tillatelse)
    return jsonify({'suksess': suksess, 'tillatelse': tillatelse})


#registrering    
@app.route("/regdata", methods=['POST'])
def registrerings_side():
    data = request.json
    brukernavn = (data.get('brukernavn'))
    passord = (data.get('passord'))
    melding, tillatelse = registrer_bruker(brukernavn, passord)
    return jsonify (melding, tillatelse)

if __name__ == "__main__":
    app.run(debug=True)
    
