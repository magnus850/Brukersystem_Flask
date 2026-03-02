# Brukersystem Web

Et brukerautentiseringssystem med innlogging, registrering og adminpanel bygget med Svelte og Flask. Alt bortsett fra styling er kodet selv, styling er vibekodet med gpt-5 mini.

## Teknologier

- **Frontend:** Svelte
- **Backend:** Flask (Python)
- **Database:** MariaDB

## Oppsett

Du må ha Python, Node.js og MariaDB konfigurert og installert fra før av. Tilpasset Mac.

Åpne terminalen og kjør disse kommandoene etter hverandre:
```bash
mkdir ikke_mitt_prosjekt && cd ikke_mitt_prosjekt
git clone https://github.com/magnus850/Brukersystem_Web && cd Brukersystem_Web
python3 -m venv venv
source venv/bin/activate
pip3 install flask flask-cors mariadb python-dotenv
```

Åpne et nytt terminalvindu og logg inn på MariaDB:
```bash
mariadb -u brukernavn -p
```

> Får du feil er det mest sannsynlig fordi MariaDB ikke kjører. Skriv `brew services start mariadb` og prøv igjen.

Kjør disse kommandoene i MariaDB:
```sql
CREATE DATABASE brukerdb;
USE brukerdb;
CREATE TABLE brukere (
    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    bruker VARCHAR(15) NOT NULL,
    passord VARCHAR(24) NOT NULL,
    tillatelse VARCHAR(20) NOT NULL DEFAULT 'bruker'
);
INSERT INTO brukere (bruker, passord, tillatelse) VALUES ('admin123', 'passord123', 'admin');
```

Tilbake i første terminal, opprett `.env`-filen:
```bash
touch .env && nano .env
```

Lim inn og fyll inn med egen MariaDB-brukerlegitimasjon:
```env
DB_BRUKER=brukernavn
DB_PASSORD=passord
DB_HOST=localhost
DB=brukerdb
```

Lagre med `Ctrl+X` -> `Y` -> `Enter`. Installer deretter frontend:
```bash
npm install svelte
```

## Kjøring

Start backend (pass på at venv er aktivert):
```bash
source venv/bin/activate
python3 backend/app.py
```

Åpne et nytt terminalvindu og start frontend:
```bash
npm run dev
```

Gå til [http://localhost:5173](http://localhost:5173) og logg inn med `admin123` / `passord123`.
