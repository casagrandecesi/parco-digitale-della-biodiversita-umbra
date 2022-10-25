# -*- coding: utf-8 -*-
#
# Questo script crea i poster delle varie risorse del
# Registro Regionale della biodiversità umbra.
#
# Le immagini vengono generate in parallelo con multiprocessing
# perché la generazione è un po' lenta

# Librerie built-in
import os
import shutil
import sqlite3
import sys

# Librerie esterne
from PIL import Image, ImageDraw, ImageFont  # type: ignore

# Libreria interna
from shape import aree


position_size = (381, 476)
credits = "Fonte: 3A - Parco Tecnologico Agroalimentare dell'Umbria"
dir_immagini = os.path.join("..", "Materiale", "Immagini")
immagine_poster_vuoto_blu = os.path.join(dir_immagini, "poster_vuoto_blu.png")
immagine_poster_vuoto_marrone = os.path.join(dir_immagini, "poster_vuoto_marrone.png")
immagine_poster_vuoto_prugna = os.path.join(dir_immagini, "poster_vuoto_prugna.png")
immagine_poster_vuoto_verde = os.path.join(dir_immagini, "poster_vuoto_verde.png")


def calcola_font_size(nome):
    # Retta che passa per (23, 140) e (66, 50)
    return int(-2.09 * len(nome) + 188.14)


def disegna_poster(immagine_poster_vuoto, riga, immagine_risorsa, immagine_posizione, immagine_rischio, immagine_destinazione):
    nome = riga["nome"]
    poster = Image.open(immagine_poster_vuoto)
    w = poster.size[0]
    illustrazione = Image.open(immagine_risorsa)
    #oldw, oldh = illustrazione.size
    #newh = int(w / oldw * oldh)
    illustrazione = illustrazione.resize((w, 887), Image.ANTIALIAS)
    poster.paste(illustrazione, (0, 0), illustrazione.convert("RGBA"))
    posizione = Image.open(immagine_posizione)
    posizione = posizione.resize((position_size))
    poster.paste(posizione, (260, 1577), posizione.convert("RGBA"))
    rischio = Image.open(immagine_rischio)
    poster.paste(rischio, (1000, 1600), rischio.convert("RGBA"))
    poster.save(immagine_destinazione)
    poster = Image.open(immagine_destinazione)
    disegno = ImageDraw.Draw(poster)
    font_size = calcola_font_size(nome)
    font_titolo = ImageFont.truetype(os.path.join("..", "Materiale", "Font", "BreeSerif-Regular.otf"), font_size)
    titw = disegno.textsize(nome, font=font_titolo)[0]
    while titw > w:
        font_size -= 5
        font_titolo = ImageFont.truetype(os.path.join("..", "Materiale", "Font", "BreeSerif-Regular.otf"), font_size)
        titw = disegno.textsize(nome, font=font_titolo)[0]
    disegno.text((w / 2, 1080), nome, fill="black", font=font_titolo, anchor="mm")
    font_credits = ImageFont.truetype(os.path.join("..", "Materiale", "Font", "BreeSerif-Regular.otf"), 50)
    disegno.text((w / 2, 2168), credits, fill="white", font=font_credits, anchor="mm")
    poster.save(immagine_destinazione)
    return immagine_destinazione


# Controlla se il database esiste
dir_dati = os.path.join("..", "Dati")
db_file = os.path.join(dir_dati, "Biodiversita.db")
if not os.path.exists(db_file):
    print("Prima devi eseguire schede.py per creare il database")
    sys.exit(1)

# Cancello la directory con i poster
# organizzati per aree
dir_poster = os.path.join("..", "Dati", "Poster")
if os.path.exists(dir_poster):
    shutil.rmtree(dir_poster)
os.makedirs(dir_poster)

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
    sezione = riga["sezione_registro"]
    print(f"{id_scheda} - {nome}")
    dir_scheda = os.path.join(dir_dati, f"Scheda_{id_scheda}")
    immagine_posizione = os.path.join(dir_scheda, "Posizione.png")
    immagine_risorsa = os.path.join(dir_scheda, "Scheda.jpg")
    immagine_rischio = os.path.join(dir_immagini, "rischio_" + riga["rischio"].lower().replace(" ", "_") + "_white.png")
    immagine_destinazione = os.path.join(dir_scheda, f"Poster_{id_scheda:02d}.png")
    if "Luccio" in nome or "Trota" in nome:
        base = immagine_poster_vuoto_blu
    elif sezione == "Vegetale":
        base = immagine_poster_vuoto_verde
    elif sezione == "Animale":
        base = immagine_poster_vuoto_marrone
    else:
        base = immagine_poster_vuoto_prugna
    immagine_poster = disegna_poster(base, riga, immagine_risorsa, immagine_posizione, immagine_rischio, immagine_destinazione)
    dir_poster_area = os.path.join(dir_poster, aree.get(id_scheda, "F"))
    if not os.path.exists(dir_poster_area):
        os.mkdir(dir_poster_area)
    poster_area = os.path.join(dir_poster_area, f"{id_scheda:02d}.png")
    shutil.copy(immagine_poster, poster_area)
    immagine_poster_3d = immagine_poster[:-4] + ".glb"
    if os.path.exists(immagine_poster_3d):
        poster_area_3d = os.path.join(dir_poster_area, f"{id_scheda:02d}.glb")
        shutil.copy(immagine_poster_3d, poster_area_3d)