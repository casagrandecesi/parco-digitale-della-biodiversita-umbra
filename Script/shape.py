# -*- coding: utf-8 -*-
#
# Questo script associa le geometrie dei vari comuni umbri
# alle risorse genetiche del Registro Regionale
#
# Lo script, inoltre, imposta l'area di pertinenza di
# ciascuna risorsa secondo questa suddivisione:
#    A: Alto Tevere
#    B: Medio Tevere
#    C: Chiascio Topino
#    D: Nera Corno
#    E: Nestòre Paglia
#    F: Tutta la regione

# Librerie built-in
import json
import os
import sqlite3
import sys

# Librerie esterne
from pyproj import Proj  # type: ignore
import shapefile  # type: ignore
import shapely.geometry  # type: ignore


# Prima definisco il dizionario con la mappa con le chiavi, perché
# è più comodo, poi lo inverto
aree_lista = {
    "A": [2, 4, 18, 37, 41, 45, 47, 50, 68, 70],
    "B": [7, 12, 14, 15, 16, 20, 27, 28, 31, 34, 35, 38, 49, 56, 68],
    "C": [11, 21, 23, 29, 30, 33, 46, 51, 55, 63, 70],
    "D": [8, 22, 25, 31, 32, 35, 43, 54, 59],
    "E": [1, 3, 10, 26, 44, 50, 67, 68, 69],
}
aree = {}
for k, v in aree_lista.items():
    for id_scheda in v:
        aree[id_scheda] = str(k)


def carica_shape_comuni(shp_file):
    reader = shapefile.Reader(shp_file, encoding="latin1")
    #first feature of the shapefile
    feature = reader.shapeRecords()
    shapes = {}
    for f in feature:
        nome_comune = f.record[3]
        shape = f.shape
        shapes[nome_comune] = shape
    return shapes


def carica_shape_regioni(shp_file):
    reader = shapefile.Reader(shp_file, encoding="latin1")
    #first feature of the shapefile
    feature = reader.shapeRecords()
    shapes = {}
    for f in feature:
        nome_regione = f.record[2]
        shape = f.shape
        shapes[nome_regione] = shape
    return shapes


# Controlla se il database esiste
dir_dati = os.path.join("..", "Dati")
db_file = os.path.join(dir_dati, "Biodiversita.db")
if not os.path.exists(db_file):
    print("Prima devi eseguire schede.py per creare il database")
    sys.exit(1)

# Carica le shape dei comuni
shp_file = os.path.join("..", "Materiale", "Shapefile Comuni", "Comuni_2011.shp")
if not os.path.exists(shp_file):
    print("Non trovo lo shapefile Comuni_2011.shp")
    sys.exit(1)
shapes = carica_shape_comuni(shp_file)

# Carica le shape delle regioni
shp_file = os.path.join("..", "Materiale", "Shapefile Regione", "Reg01012022_g_WGS84.shp")
if not os.path.exists(shp_file):
    print("Non trovo lo shapefile Reg01012022_g_WGS84.shp")
    sys.exit(1)
shape_regioni = carica_shape_regioni(shp_file)

# Leggiamo tutte le righe del database
con = sqlite3.connect(db_file)
# Accesso alle colonne sia con indice numerico che con nome
con.row_factory = sqlite3.Row
cur = con.cursor()
cur.execute("SELECT * FROM Biodiversita")
righe = cur.fetchall()
for riga in righe:
    # Leggiamo il nome
    nome = riga["nome"]
    print("SET PUNTI:", nome)
    
    # Leggiamo l'ambito locale
    ambito_locale = riga["ambito_locale"]
    if "Comprensorio del Trasimeno" in ambito_locale:
        ambito_locale = "Comuni di Castiglione del Lago, Passignano sul Trasimeno, Tuoro sul Trasimeno, Magione, Città della Pieve, Piegaro, Corciano, Panicale, Paciano"
    elif "Comuni del Comprensorio della Valnerina" in ambito_locale:
        ambito_locale = "Comuni di Norcia, Cascia, Cerreto di Spoleto, Monteleone di Spoleto, Poggiodomo, Preci, Sant’Anatolia di Narco, Scheggino, Vallo di Nera, Arrone, Ferentillo, Polino"
    elif ambito_locale == "Frazione di Cave di Foligno (PG)":
        ambito_locale = "Comune di Foligno"
    elif ambito_locale == "Frazione di Camerata di Todi (PG)":
        ambito_locale = "Comune di Todi"
    elif nome == "Fagiolo Morone di Macenano":
        ambito_locale = "Comune di Ferentillo"
    elif nome == "Farro di Monteleone di Spoleto":
        ambito_locale = "Comune di Monteleone di Spoleto"
    elif nome == "Fagiolo Secondi del Piano":
        ambito_locale = "Comune di Orvieto"
    elif nome == "Lievito CMCR 102 – Sagrantino 1":
        ambito_locale = "Comuni di Montefalco, Bevagna, Gualdo Cattaneo, Castel Ritaldi, Giano dell'Umbria"
    elif nome == "Olivo Gentile Grande":
        ambito_locale = "Comuni di San Giustino, Citerna, Monte Santa Maria Tiberina, Città di Castello, Umbertide, Montone, Pietralunga"
    elif nome == "Olivo Peperina":
        ambito_locale = "Comuni di Gubbio, Perugia"
    elif nome == "Olivo Gnacolo":
        ambito_locale = "Comuni di Assisi, Spello, Valtopina"
    
    # Associamo le shape dei vari comuni/regione
    if ambito_locale == "Regione Umbria":
        shape_list = [shape_regioni["Umbria"].__geo_interface__]
    elif ambito_locale.startswith("Comuni di ") or ambito_locale.startswith("Comune di "):
        comuni = [c.upper().strip() for c in ambito_locale[len("Comun* di "):].replace(" e ", ",").replace(".", "").replace("à", "a'").replace("’", "'").split(",")]
        shape_list = []
        for c in comuni:
            # Converto i nomi dei comuni in quelli contenuti nello shapefile
            if c == "SCHEGGIA":
                c = "SCHEGGIA E PASCELUPO"
            elif c == "MONTELEONE DI ORVIETO":
                c = "MONTELEONE D'ORVIETO"
            elif c == "CALVI":
                c = "CALVI DELL'UMBRIA"
            elif c == "CESI":
                c = "TERNI"
            elif c == "LUGNANO":
                c = "LUGNANO IN TEVERINA"
            elif c == "MONTE S MARIA TIBERINA":
                c = "MONTE SANTA MARIA TIBERINA"
            elif c in ("S GIUSTINO", "SAN GIUSTINO UMBRO"):
                c = "SAN GIUSTINO"
            elif c == "MONTECASTELLO VIBIO":
                c = "MONTE CASTELLO DI VIBIO"
            shape = shapes[c].__geo_interface__
            shape_list.append(shape)
    else:
        print("Ambito locale non previsto:", ambito_locale)
        sys.exit(1)
    print ("AMBITO LOCALE:", ambito_locale)
    # Salvo la shape nel database
    shape_str = json.dumps(shape_list)
    cur.execute("UPDATE Biodiversita SET shape = ? WHERE id = ?", (shape_str, riga["id"]))
    # Salvo le coordinate dei punti rappresentativi nel database
    if ambito_locale == "Regione Umbria":
        cur.execute("UPDATE Biodiversita SET punti = '', area = 'F' WHERE id = ?", (riga["id"],))
    else:
        punti = []
        for sh in shape_list:
            sh_geom = shapely.geometry.shape(sh)
            punti.append((sh_geom.centroid.x, sh_geom.centroid.y))
        punti_str = json.dumps(punti)
        id_scheda = riga["id"]
        area = aree[id_scheda]
        print(riga["id"], " POINTS --->", len(punti))
        cur.execute("UPDATE Biodiversita SET punti = ?, area = ? WHERE id = ?", (punti_str, area, id_scheda))

# Salviamo le modifiche
con.commit()

# Facciamo un piccolo test con delle coordinate fisse
# Si noti che lo shapefile dei comuni usa EPSG:23032 - ED50 / UTM zone 32N
my_proj = Proj(proj='utm', zone=32, ellps='WGS84', preserve_units=True)
utm_x, utm_y = my_proj(12.243889, 43.460833)    # Citta' di Castello
print("UTM:", utm_x, utm_y)
test_point = shapely.geometry.Point(utm_x, utm_y)
cur.execute("SELECT * FROM Biodiversita")
righe = cur.fetchall()
for riga in righe:
    shape_str = riga["shape"]
    if not shape_str:
        continue
    shape_list = json.loads(shape_str)
    for shape in shape_list:
        shp_geom = shapely.geometry.shape(shape)
        if shp_geom.contains(test_point):
            nome = riga["nome"]
            print(nome)

cur.close()
con.close()