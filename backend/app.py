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
CORS(app, resources={r"/*": {"origins": "*"}})

def bruker_sjekk(brukernavn, passord):
    cur.execute(
        'SELECT id, passord, tillatelse FROM brukere WHERE bruker =%s AND passord = %s',
        (brukernavn, passord))
    resultat = cur.fetchone()
    if resultat == None:
        suksess = False
        return suksess, None, None 
    elif resultat: 
        resultat_liste = list(resultat)
        tillatelse = resultat_liste[2]
        id = resultat_liste[0]
        suksess = True
        return suksess, tillatelse, id
    
    
def registrer_bruker(brukernavn, passord):
    cur.execute('select bruker from brukere where bruker = %s',
            (brukernavn,))
    resultat = cur.fetchone()
    if resultat != None:
        return 'Brukernavn er tatt, velg et annet', None, None
    elif resultat == None: 
        cur.execute(
        'insert into brukere (bruker, passord) values (%s, %s)',
        (brukernavn, passord))
        conn.commit()
        cur.execute(
            'select tillatelse from brukere where bruker =%s',
            (brukernavn,))
        tillatelse = cur.fetchone()
        return None, brukernavn, tillatelse

def alle_brukere(brukernavn):
    cur.execute("select id, bruker, tillatelse from brukere where bruker !=%s",
                (brukernavn,))
    return cur.fetchall()
    
def slett_bruker_fra_db(id):
    int_id = int(id)
    print (int_id)
    cur.execute("delete from brukere where id =%s",
                (int_id,))
    conn.commit()
    return True

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
    suksess, tillatelse, id = bruker_sjekk(brukernavn, passord)
    print(suksess, tillatelse, id)
    return jsonify({'suksess': suksess, 'tillatelse': tillatelse, 'id': id})

#registrering    
@app.route("/regdata", methods=['POST'])
def registrerings_side():
    data = request.json
    brukernavn = (data.get('brukernavn'))
    passord = (data.get('passord'))
    melding, brukernavn, tillatelse, id = registrer_bruker(brukernavn, passord)
    return jsonify ({'melding': melding, 'brukernavn': brukernavn, 'tillatelse': tillatelse, 'id': id})

#brukeroversikt for admins
@app.route("/brukerdb", methods=['POST'])
def hent_brukere():
    data = request.json
    brukernavn = (data.get('brukernavn'))
    brukere = alle_brukere(brukernavn)
    return jsonify ({'brukere': brukere})

#sletting av brukere for admins
@app.route("/slettbruker", methods=['POST'])
def slett_bruker():
    data = request.json
    id = data.get('id')
    bruker_slettet = slett_bruker_fra_db(id)
    return jsonify ({'brukerslettet': bruker_slettet})

if __name__ == "__main__":
    app.run(debug=False)
    
