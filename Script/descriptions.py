# -*- coding: utf-8 -*-
#
# Questo script recupera le descrizioni brevi dalle singole pagine HTML
# scaricate con lo script schede.py e le salva nel database

import codecs
import os
import sqlite3

from bs4 import BeautifulSoup  # type: ignore


def estrai_id(dir_scheda):
    # Ottimismo
    return int(dir_scheda[len("Scheda_"):])


def get_file_schede_html(dir_dati):
    file_schede = {}
    for dir_scheda in os.listdir(dir_dati):
        if not dir_scheda.startswith("Scheda_"):
            continue
        dir_scheda_abs = os.path.join(dir_dati, dir_scheda)
        file_scheda_html = os.path.join(dir_scheda_abs, "Scheda.html")
        id_scheda = estrai_id(dir_scheda)
        file_schede[id_scheda] = file_scheda_html
    return file_schede


def estrai_descrizione(file_scheda):
    testi = []
    with codecs.open(file_scheda, encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        pt2 = soup.find("div", class_="pt-2")
        p_list = pt2.find_all("p")
        for p in p_list:
            testi.append(p.getText())
    return "\n".join(testi)


dir_dati = os.path.join("..", "Dati")
db_file = os.path.join(dir_dati, "Biodiversita.db")
con = sqlite3.connect(db_file)
cur = con.cursor()
file_schede = get_file_schede_html(dir_dati)
for i, f in file_schede.items():
    # Casi particolari
    if i == 9:  # Olivo Moraiolo
        descrizione = "Varietà coltivata nell'intero territorio olivicolo regionale, ove rappresenta la cultivar tradizionale più diffusa. Essa rappresenta almeno il 90% del patrimonio olivicolo storico della fascia olivata compresa tra Assisi e Spoleto, fino alla conca Ternana."
    elif i == 10:  # Olivo Dolce Agogia
        descrizione = "Varietà coltivata sulle Colline del Trasimeno e dei comuni del comprensorio Perugino. Sporadicamente presente anche nelle restanti parti del territorio Regionale. Rappresenta la maggioranza del patrimonio olivicolo dei comuni di Perugia, Umbertide, Corciano, Montone e di tutti quelli prospicienti il lago Trasimeno"
    elif i == 11:  # Olivo Nostrale di Rigali
        descrizione = "Varietà diffusa lungo la fascia pedemontana del comprensorio nord-orientale dell'Umbria. Rappresenta la maggioranza del patrimonio olivicolo dei comuni di Gualdo Tadino, Nocera Umbra e Gubbio. La cultivar è presente anche nei Comuni di Fossato di Vico, Sigillo, Costacciaro, Scheggia e Pascelupo."
    elif i == 12:  # Vitigno Grero
        descrizione = "Il nome deriva dalla fusione delle due parole che compongono il nome con cui la varietà è localmente nota: Greco nero, da cui Grero"
    elif i == 13:  # Cavallo agricolo italiano da tiro pesante rapido (T.P.R.)
        descrizione = "Gli allevamenti si sono diffusi con maggiore concentrazione in Veneto, in Emilia Romagna, in Umbria, nel lazio, in Abruzzo e in Puglia; discrete numerosità si hanno in Friuli, nelle Marche, in Toscana, in Molise e in Campania. Allevamenti più isolati ma molto attivi dal punto di vista selettivo sono presenti in Piemonte, Lombardia, Trentino e Basilicata."
    elif i == 70:  # Lievito CMCR 102 – Sagrantino 1
        descrizione = "Il nome rimanda alla sigla del Centro dove il ceppo è conservato, Cemin Microbial Collection, mentre il termine “Sagrantino 1” fa riferimento all’areale di vinificazione dove il ceppo è stato selezionato"
    else:
        descrizione = estrai_descrizione(f)
    sql = "UPDATE Biodiversita SET descrizione = ? WHERE id = ?"
    cur.execute(sql, (descrizione, i))
# Chiudiamo la connessione al database
con.commit()
cur.close()
con.close()
