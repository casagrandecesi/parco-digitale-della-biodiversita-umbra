# -*- coding: utf-8 -*-
#
# Questo script scarica le schede delle varie risorse genetiche
# iscritte nel Registro Regionale della Regione Umbria

# Librerie built-in
import codecs
import csv
import os
import sqlite3

# Librerie esterne
from bs4 import BeautifulSoup  # type: ignore
import requests  # type: ignore


# Se la directory "Schede" non esiste, creiamola!
dir_dati = os.path.join("..", "Dati")
if not os.path.exists(dir_dati):
    os.mkdir(dir_dati)
# Se il database SQLite3 non esiste, creiamolo!
db_file = os.path.join(dir_dati, "Biodiversita.db")
if os.path.exists(db_file):
    os.unlink(db_file)
con = sqlite3.connect(db_file)
cur = con.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS Biodiversita (
    id INTEGER,
    nome TEXT,
    rischio TEXT,
    data_iscrizione TEXT,
    ambito_locale TEXT,
    modica_quantita TEXT,
    sezione_registro TEXT,
    tipologia_risorsa TEXT,
    famiglia TEXT,
    genere TEXT,
    specie TEXT,
    nome_comune TEXT,
    significato_nome TEXT,
    sinonimi TEXT,
    nome_dialettale TEXT,
    luogo_conservazione TEXT,
    descrizione TEXT,
    scheda_portale TEXT,
    shape TEXT,
    punti TEXT,
    area TEXT,
    PRIMARY KEY (id)
);""")
# Apriamo il file CSV in lettura
file_csv = os.path.join("..", "Materiale", "biodiversitaV2.csv")
with codecs.open(file_csv, encoding="utf-8") as f:
    # Associamo il file CSV ad un "parser" che sa gestirne la struttura
    csv_reader = csv.reader(f, delimiter=',')
    for i, linea in enumerate(csv_reader):
        # Ignora la prima linea, è il titolo
        if i == 0:
            continue
        # Converto l'identificativo da testo a numero intero
        # Tutti gli altri campi, invece, restano di tipo testo
        print(f"{linea[0]} - {linea[1]}")
        linea[0] = int(linea[0])
        # Normalizzo i livelli di rischio
        # Dopo la normalizzazione i livelli di rischio sono:
        # - Elevato, Medio, Non a rischio
        # - Critico, Minacciata, Non a rischio
        # Si noti che "Critico" (per fortuna) non è utilizzato e che
        # nella StoryMap "Minacciata" viene indicato in rosso
        if linea[2] == "Alto":
            linea[2] = "Elevato"
        elif linea[2] == "Minacciata di abbandono":
            linea[2] = "Minacciata"
        # Usiamo soltanto tre livelli per comodità
        elif linea[2] == "Medio - Basso":
            linea[2] = "Medio"
        # Sia i Fagioli Secondi del Piano (44) che il Vitigno Dolciame (50) hanno
        # un rischio "Medio alto"; tuttavia questo rischio è stato normalizzato
        # nella StoryMap come Elevato in un caso e Medio nell'altro
        elif linea[0] == 44:
            linea[2] = "Elevato"
        elif linea[0] == 50:
            linea[2] = "Medio"
        # Normalizzo la data d'inserimento trasformandola in formato ISO 8601
        if linea[0] == 1:
            linea[3] = "2013-11-11"
        else:
            # Da 15/03/2022 a 2022-03-15
            v = linea[3].split("/")
            linea[3] = v[2] + "-" + v[1] + "-" + v[0]
        # Inserisco la riga nel database
        sql = "INSERT INTO Biodiversita VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,'',?,'','', '')"
        cur.execute(sql, linea)
        # Creo una directory per ospitare i dati della scheda
        id_scheda = linea[0]
        dir_scheda = os.path.join(dir_dati, f"Scheda_{id_scheda}")
        # Se la directory della scheda esiste assumo di averla già scaricata
        # Se volessi riscaricarla dovrei cancellare la directory...
        if os.path.exists(dir_scheda):
            continue
        else:
            os.mkdir(dir_scheda)
        # Scarico la scheda in formato HTML
        url_scheda_html = linea[16]
        scheda_html = requests.get(url_scheda_html)
        file_scheda_html = os.path.join(dir_scheda, "Scheda.html")
        with codecs.open(file_scheda_html, "w", encoding="utf-8") as f:
            f.write(scheda_html.text)
        # Trovo l'URL della scheda in formato PDF
        soup = BeautifulSoup(scheda_html.text, 'html.parser')
        anchors = soup.find_all('a')
        url_scheda_pdf = None
        for a in anchors:
            if a["href"].endswith(".pdf"):
                url_scheda_pdf = a["href"]
                break
        # Scarico la scheda in formato PDF
        if url_scheda_pdf:
            scheda_pdf = requests.get(url_scheda_pdf)
            file_scheda_pdf = os.path.join(dir_scheda, "Scheda.pdf")
            with open(file_scheda_pdf, "wb") as f:
                f.write(scheda_pdf.content)
        # Trovo l'URL dell'immagine principale della scheda
        img = soup.find_all("img", class_="immagine-risorsa")
        if img:
            url_img = img[-1]["src"]
            img_data = requests.get(url_img)
            file_img = os.path.join(dir_scheda, "Scheda.jpg")
            with open(file_img, "wb") as f:
                f.write(img_data.content)
# Chiudiamo la connessione al database
con.commit()
cur.close()
con.close()
