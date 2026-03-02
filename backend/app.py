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
    **({"unix_socket": os.getenv('DB_SOCKET')} if os.getenv('DB_SOCKET') else {})
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
        return 'Brukernavn er tatt, velg et annet', None, None, None
    elif resultat == None: 
        cur.execute(
        'insert into brukere (bruker, passord) values (%s, %s)',
        (brukernavn, passord))
        conn.commit()
        cur.execute(
            'select tillatelse, id from brukere where bruker =%s',
            (brukernavn,))
        tillatelse_id= cur.fetchone()
        return None, brukernavn, tillatelse_id[0], tillatelse_id[1]

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

def endre_passord_db(id, nytt_passord):
    cur.execute('select * from brukere where passord =%s and id=%s',
                (nytt_passord, id))
    resultat = cur.fetchone()
    if resultat != None:
        return False
    elif resultat == None:
        cur.execute('update brukere set passord =%s where id=%s',
        (nytt_passord, id))
        conn.commit()
        return True
    
def endre_tillatelse(id):
    cur.execute('update brukere set tillatelse=%s where id=%s',
                ('admin', id))
    conn.commit()
    return "Vellykket tillatelse-endring"

#routes
@app.route("/")
def forside_route():
    cur.execute("select * from brukere;")
    data = cur.fetchall()
    return jsonify({"brukere":data})

#innlogging
@app.route("/inputdata", methods=['POST'])
def logg_inn_side_route():
    data = request.json
    brukernavn = (data.get('brukernavn'))
    passord = (data.get('passord'))
    suksess, tillatelse, id = bruker_sjekk(brukernavn, passord)
    return jsonify({'suksess': suksess, 'tillatelse': tillatelse, 'id': id})

#registrering    
@app.route("/regdata", methods=['POST'])
def registrerings_side_route():
    data = request.json
    brukernavn = (data.get('brukernavn'))
    passord = (data.get('passord'))
    melding, brukernavn, tillatelse, id = registrer_bruker(brukernavn, passord)
    return jsonify ({'melding': melding, 'brukernavn': brukernavn, 'tillatelse': tillatelse, 'id': id})

#brukeroversikt for admins
@app.route("/brukerdb", methods=['POST'])
def hent_brukere_route():
    data = request.json
    brukernavn = (data.get('brukernavn'))
    brukere = alle_brukere(brukernavn)
    return jsonify ({'brukere': brukere})

#sletting av brukere for admins
@app.route("/slettbruker", methods=['POST'])
def slett_bruker_route():
    data = request.json
    id = data.get('id')
    bruker_slettet = slett_bruker_fra_db(id)
    return jsonify ({'brukerslettet': bruker_slettet})

@app.route("/endrepassord", methods=['POST'])
def endre_passord_route():
    data = request.json
    id = data.get('id')
    nytt_passord = data.get('nytt_passord')
    passord_endret = endre_passord_db(id, nytt_passord)
    return jsonify ({'passordendret': passord_endret})

@app.route("/tillatelseendring", methods=['POST'])
def endre_tillatelse_route():
    data=request.json
    id = data.get('id')
    melding = endre_tillatelse(id)
    return melding
    
if __name__ == "__main__":
    app.run(debug=True)
    
