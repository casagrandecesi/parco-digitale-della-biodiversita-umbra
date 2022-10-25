# -*- coding: utf-8 -*-
#
# Questo script crea le immagini dell'Umbria con le posizioni
# geografiche dei vari elementi del registro della biodiversità

# Librerie built-in
import json
import os
import shutil
import sqlite3
import sys

# Librerie esterne
from PIL import Image, ImageDraw  # type: ignore


# Bounding box dell'Umbria (da SW a NE) in UTM 32N
umbria_wx = 736978.044
umbria_sy = 4696471.61
umbria_ex = 848750.97
umbria_ny = 4835045.001


def disegna_coordinate(lista_coordinate, file_destinazione):    
    umbria = Image.open(os.path.join("..", "Materiale", "Immagini", "umbria_white.png"))
    disegno = ImageDraw.Draw(umbria)
    maxx, maxy = umbria.size
    for utmx, utmy in lista_coordinate:
        x = (utmx - umbria_wx) * maxx / (umbria_ex - umbria_wx)
        y = maxy - (maxy * (utmy - umbria_sy) / (umbria_ny - umbria_sy))
        raggio = max(maxx, maxy) / 30
        disegno.ellipse((x - raggio, y - raggio, x + raggio, y + raggio), fill='#8badb4', outline='#8badb4')
    umbria.save(file_destinazione)


# ESEMPIO
# ---------------------------------------------------
# lista_coordinate = [
#     (43.460833, 12.243889),  # Città di Castello
#     (42.65, 12.483333),      # Montecastrilli
#     (42.793333, 13.093889),  # Norcia
# ]
# disegna_coordinate(lista_coordinate, "test.png")

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
umbria_blu = os.path.join("..", "Materiale", "Immagini", "umbria_blu.png")
for riga in righe:
    id_scheda = riga["id"]
    nome = riga["nome"]
    print(f"{id_scheda} - {nome}")
    dir_scheda = os.path.join(dir_dati, f"Scheda_{id_scheda}")
    immagine = os.path.join(dir_scheda, "Posizione.png")
    if not riga["punti"]:
        shutil.copy(umbria_blu, immagine)
    else:
        punti = json.loads(riga["punti"])
        disegna_coordinate(punti, immagine)
