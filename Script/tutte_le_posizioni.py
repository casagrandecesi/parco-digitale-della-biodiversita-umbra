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

immagine_originale = os.path.join("..", "Materiale", "Immagini", "aree.png")
immagine_di_lavoro = os.path.join("..", "Materiale", "Immagini", "umbria_tutte.png")


def disegna_coordinate(id_scheda, lista_coordinate, file_destinazione):    
    umbria = Image.open(immagine_di_lavoro)
    disegno = ImageDraw.Draw(umbria)
    maxx, maxy = umbria.size
    for utmx, utmy in lista_coordinate:
        x = (utmx - umbria_wx) * maxx / (umbria_ex - umbria_wx)
        y = maxy - (maxy * (utmy - umbria_sy) / (umbria_ny - umbria_sy))
        raggio = max(maxx, maxy) / 60
        disegno.ellipse((x - raggio, y - raggio, x + raggio, y + raggio), fill='blue', outline='blue')
        disegno.text((x - 5, y - 5), str(id_scheda))  # Numeri scelti empiricamente
        print(x, y)
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

# Resetta l'immagine di lavoro
shutil.copy(immagine_originale, immagine_di_lavoro)

# Leggiamo tutte le righe del database
con = sqlite3.connect(db_file)
# Accesso alle colonne sia con indice numerico che con nome
con.row_factory = sqlite3.Row
cur = con.cursor()
cur.execute("SELECT * FROM Biodiversita")
righe = cur.fetchall()
for riga in righe:
    id_scheda = riga["id"]
    nome = riga["nome"]
    print(f"{id_scheda} - {nome}")
    if riga["punti"]:
        punti = json.loads(riga["punti"])
        disegna_coordinate(id_scheda, punti, immagine_di_lavoro)
