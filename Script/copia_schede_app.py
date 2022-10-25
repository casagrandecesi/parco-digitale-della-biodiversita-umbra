import os
import shutil

dir_dati = os.path.join("..", "Dati")
dir_www = os.path.join("..", "App", "www", "schede")
sotto_dir_dati = os.listdir(dir_dati)
for sdd in sotto_dir_dati:
    if not sdd.startswith("Scheda_"):
        continue
    d = os.path.join(dir_dati, sdd)
    n = sdd.split("_")[1]
    dd = os.path.join(dir_www, n)
    if not os.path.exists(dd):
        os.mkdir(dd)
    shutil.copy(os.path.join(d, "Scheda.jpg"), os.path.join(dd, "immagine.jpg"))
    shutil.copy(os.path.join(d, "Posizione.png"), os.path.join(dd, "posizione.png"))
    shutil.copy(os.path.join(d, "Scheda.pdf"), os.path.join(dd, "scheda.pdf"))
