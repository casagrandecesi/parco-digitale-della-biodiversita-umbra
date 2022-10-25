# -*- coding: utf-8 -*-
#
# Questo script crea una struttura dati JSON dentro
# un file JavaScript per l'uso tramite app

# Librerie built-in
import datetime
import json
import os
import sqlite3
import sys


# Controlla se il database esiste
dir_dati = os.path.join("..", "Dati")
db_file = os.path.join(dir_dati, "Biodiversita.db")
if not os.path.exists(db_file):
    print("Prima devi eseguire schede.py per creare il database")
    sys.exit(1)

# Leggiamo tutte le righe del database
con = sqlite3.connect(db_file)
# Accesso alle colonne sia con indice numerico che con nome
con.row_factory = sqlite3.Row
cur = con.cursor()
cur.execute("SELECT * FROM Biodiversita")
righe = cur.fetchall()
chiavi = righe[0].keys()
dati = []
for riga in righe:
    dati.append({k: riga[k] for k in chiavi})
file_json = "biodiversita.js"
with open(file_json, "w") as f:
    print("Salvo i dati JSON in", file_json)
    f.write("// Generato in data ")
    f.write(datetime.datetime.now().isoformat())
    f.write("\n")
    f.write("biodiversita = ")
    json.dump(dati, f)
    f.write(";")
