/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */

// Wait for the deviceready event before using any of Cordova's device APIs.
// See https://cordova.apache.org/docs/en/latest/cordova/events/events.html#deviceready
document.addEventListener('deviceready', onDeviceReady, false);

var FACILE = 1;
var INTERMEDIO = 2;
var DIFFICILE = 3;
var NUMERO_DOMANDE = 10;

var bottoneScopri = document.getElementById("bottone-scopri");
var bottoneQuiz = document.getElementById("bottone-quiz");
var cerca = document.getElementById("cerca");
var risultati = document.getElementById("risultati");
var quiz = document.getElementById("quiz");
var fogliolina = document.getElementById("fogliolina");
var bottoneIndietro = document.getElementById("bottone-indietro");
var informazioni = document.getElementById("informazioni");
var about = document.getElementById("about");
var erroregps = document.getElementById("erroregps");
var caricamento = document.getElementById("caricamento");
var bottoneQuizFacile = document.getElementById("bottone-quiz-facile");
var bottoneQuizIntermedio = document.getElementById("bottone-quiz-intermedio");
var bottoneQuizDifficile = document.getElementById("bottone-quiz-difficile");
var quizIntro = document.getElementById("quiz-intro");
var quizDomanda = document.getElementById("quiz-domanda");
var quizRisultato = document.getElementById("quiz-risultato");
var domande = [];
var indiceDomanda = 0;
var punti = 0;
var spanIndiceDomanda = document.getElementById("indice-domanda");
var spanNumeroDomande = document.getElementById("numero-domande");
var quizNome = document.getElementById("quiz-nome");
var quizImmagine = document.getElementById("quiz-immagine");
var quizRispostaCorretta = document.getElementById("quiz-risposta-corretta");
var quizRispostaSbagliata = document.getElementById("quiz-risposta-sbagliata");
var bottoneQuizRisposta1 = document.getElementById("bottone-quiz-risposta-1");
var bottoneQuizRisposta2 = document.getElementById("bottone-quiz-risposta-2");
var bottoneQuizRisposta3 = document.getElementById("bottone-quiz-risposta-3");
var quizRisultatoPunteggio = document.getElementById("quiz-risultato-punteggio");
var quizRisultatoMessaggio = document.getElementById("quiz-risultato-messaggio");
var quizRisultatoImmagine = document.getElementById("quiz-risultato-immagine");
var bottoneFineQuiz = document.getElementById("bottone-fine-quiz");

function isPointInside(x, y, polygon) {
    let inside = false;
    for (let i = 0, j = polygon.length - 1; i < polygon.length; j = i++) {
        const xi = polygon[i][0]; const yi = polygon[i][1];
        const xj = polygon[j][0]; const yj = polygon[j][1];
        const intersect = ((yi > y) !== (yj > y)) && (x < (xj - xi) * (y - yi) / (yj - yi) + xi);
        if (intersect) inside = !inside;
    }
    return inside
}

function pointInPolygon(polygon, point) {
    //A point is in a polygon if a line from the point to infinity crosses the polygon an odd number of times
    let odd = false;
    //For each edge (In this case for each point of the polygon and the previous one)
    for (let i = 0, j = polygon.length - 1; i < polygon.length; i++) {
        //If a line from the point into infinity crosses this edge
        if (((polygon[i][1] > point[1]) !== (polygon[j][1] > point[1])) // One point needs to be above, one below our y coordinate
            // ...and the edge doesn't cross our Y corrdinate before our x coordinate (but between our x coordinate and infinity)
            && (point[0] < ((polygon[j][0] - polygon[i][0]) * (point[1] - polygon[i][1]) / (polygon[j][1] - polygon[i][1]) + polygon[i][0]))) {
            // Invert odd
            odd = !odd;
        }
        j = i;
    }
    //If the number of crossings was odd, the point is in the polygon
    return odd;
};

function trovaArea(lat, lon) {
    // Conversione coordinate WGS84 ---> UTM
    proj4.defs("EPSG:32632","+proj=utm +zone=32"); // https://epsg.io/32632
    sourceProj = new proj4.Proj('WGS84');
    destProj = new proj4.Proj('EPSG:32632');

    var p = new proj4.toPoint([lon, lat]);
    var r = proj4.transform(sourceProj, destProj, p);
    console.log("UTM:", r.x, r.y)
    var turf_point = turf.point([r.x, r.y]);
    var found = [];
    for (var i = 0; i < biodiversita.length; ++i) {
        var shape = JSON.parse(biodiversita[i]["shape"]);
        var inside = false;
        for (let shape_index = 0; shape_index < shape.length; ++shape_index) (function () {
            var poly = shape[shape_index];
            if (poly.type == "Polygon") {
                poly.coordinates = [poly.coordinates];
            }
            for (var coord_index = 0; coord_index < poly.coordinates.length; ++coord_index) (function () {
                var sub_poly = poly.coordinates[coord_index];
                var turf_poly = turf.polygon(sub_poly);
                inside = inside || turf.booleanContains(turf_poly, turf_point);
            })();
        })();
        if (inside) {
            found.push(biodiversita[i])
        }
    }
    // Ordina per area (preferito) e nome
    // In questo modo le risorse dell'area F (tutta la regione)
    // vanno in fondo
    found.sort(function (a, b) {
        if (a["area"] == b["area"] && a["nome"] == b["nome"]) return 0;
        else if (a["area"] < b["area"] || ((a["area"] == b["area"]) && (a["nome"] < b["nome"]))) return -1;
        else return 1;
    });
    return found;
}

// Grazie a https://stackoverflow.com/questions/494143/creating-a-new-dom-element-from-an-html-string-using-built-in-dom-methods-or-pro
function htmlToElement(html) {
    var template = document.createElement('template');
    html = html.trim(); // Never return a text node of whitespace as the result
    template.innerHTML = html;
    return template.content.firstChild;
}

function creaCard(riga) {
    var card = '' +
        '<div class="card" style="margin: 20px 0">' +
        '<img src="schede/' + riga["id"] + '/immagine.jpg" class="card-img-top">' +
        '<div class="card-body">' +
        '<div class="row">' +
        '<div class="col">' +
        '    <h5 class="card-title">' + riga["nome"] + '</h5>' +
        '    <p class="card-text">Rischio: ' + riga["rischio"] + '</p>' +
        '    <a href="' + riga["scheda_portale"] + '" class="btn btn-primary">Dettagli</a>' +
        '</div>' +
        '<div class="col align-middle">' +
        '<img src="schede/' + riga["id"] + '/posizione.png" width="100">' +
        '</div>' +
        '</div>' +
        '</div>' +
        '</div>';
    return htmlToElement(card);
}

function nascondiTutto() {
    erroregps.style.display = "none";
    about.style.display = "none";
    cerca.style.display = "none";
    risultati.style.display = "none";
    quiz.style.display = "none";
    fogliolina.style.display = "none";
    bottoneIndietro.style.display = "none";
    fogliolina.style.display = "none";
    caricamento.style.display = "none";
}

function cercaBiodiversita(lat, lon) {
    var found = trovaArea(lat, lon);
    if (found.length > 0) {
        risultati.innerHTML = "";  // Pulisci la lista dei risultati
        for (var i = 0; i < found.length; ++i) (function () {
            var card = creaCard(found[i]);
            risultati.append(card);
        })();
    } else {
        risultati.innerHTML = '<div id="cerca" class="bg-light p-5 rounded">' +
                              '<h2>Scopri la biodiversità umbra</h2>' +
                              '<p>Vieni in Umbria e scopri la ricchezza della' +
                              'biodiversità regionale!</p>';
    }
    nascondiTutto();
    risultati.style.display = "block";
    bottoneIndietro.style.display = "block";
}

function riproduci(mp3) {
    var audio = new Audio(mp3);
    audio.play();
}

function mescola(arr) {
    arr.sort(function () { return Math.random() - 0.5 });
}

function iniziaQuiz(livello) {
    quizIntro.style.display = "none";
    quizDomanda.style.display = "block";
    quizRisultato.style.display = "none";

    indiceDomanda = 0;
    punti = 0;

    var vegetale = biodiversita.filter(function(x) { return x.sezione_registro === "Vegetale"; });
    mescola(vegetale);
    var animale = biodiversita.filter(function(x) { return x.sezione_registro === "Animale"; });
    mescola(animale);

    if (livello == FACILE) domande = animale.slice(0, NUMERO_DOMANDE);
    if (livello == INTERMEDIO) {
        domande = animale.slice(0, NUMERO_DOMANDE / 2).concat(vegetale.slice(0, NUMERO_DOMANDE / 2));
        mescola(domande);
    }
    if (livello == DIFFICILE) domande = vegetale.slice(0, NUMERO_DOMANDE);

    for (var i = 0; i < NUMERO_DOMANDE; ++i) (function () {
        var risposte = [domande[i].nome];
        for (var k = 0; k < 2; ++k) (function () {
            var candidata = null;
            while (candidata === null) {
                var x = biodiversita[Math.floor(Math.random() * biodiversita.length)];
                if (!risposte.includes(x.nome) && x.sezione_registro === domande[i].sezione_registro) {
                    candidata = x.nome;
                }
            }
            risposte.push(candidata);
        })();
        mescola(risposte);
        domande[i].risposte = risposte;
    })();
    mostraDomanda();
}

function resetBottoneDomanda(bottone) {
    bottone.classList.remove("btn-outline-success");
    bottone.classList.remove("btn-outline-danger");
    bottone.classList.add("btn-secondary");
}

function bottoneRispostaCorretta(bottone) {
    bottone.classList.remove("btn-secondary");
    bottone.classList.add("btn-outline-success");
}

function bottoneRispostaSbagliata(bottone) {
    bottone.classList.remove("btn-secondary");
    bottone.classList.add("btn-outline-danger");
}

function mostraDomanda() {
    var domanda = domande[indiceDomanda];
    spanIndiceDomanda.innerHTML = indiceDomanda + 1;
    spanNumeroDomande.innerHTML = NUMERO_DOMANDE;
    quizRispostaCorretta.style.display = "none";
    quizRispostaSbagliata.style.display = "none";
    quizNome.innerHTML = domanda.sezione_registro;
    quizImmagine.src = "schede/" + domanda.id + "/immagine.jpg";
    bottoneQuizRisposta1.innerHTML = domanda.risposte[0];
    resetBottoneDomanda(bottoneQuizRisposta1);
    bottoneQuizRisposta2.innerHTML = domanda.risposte[1];
    resetBottoneDomanda(bottoneQuizRisposta2);
    bottoneQuizRisposta3.innerHTML = domanda.risposte[2];
    resetBottoneDomanda(bottoneQuizRisposta3);
}

function mostraRisposta(risposta) {
    var domanda = domande[indiceDomanda];
    if (bottoneQuizRisposta1.innerHTML === domanda.nome) bottoneRispostaCorretta(bottoneQuizRisposta1);
    else bottoneRispostaSbagliata(bottoneQuizRisposta1);
    if (bottoneQuizRisposta2.innerHTML === domanda.nome) bottoneRispostaCorretta(bottoneQuizRisposta2);
    else bottoneRispostaSbagliata(bottoneQuizRisposta2);
    if (bottoneQuizRisposta3.innerHTML === domanda.nome) bottoneRispostaCorretta(bottoneQuizRisposta3);
    else bottoneRispostaSbagliata(bottoneQuizRisposta3);
    if (risposta === domanda.nome) {
        ++punti;
        quizRispostaCorretta.display = "block";
        riproduci("snd/correct.mp3");
    } else {
        quizRispostaSbagliata.display = "block";
        riproduci("snd/buzzer.mp3");
    }
    ++indiceDomanda;
    setTimeout(function () {
        if (indiceDomanda == NUMERO_DOMANDE) mostraRisultato();
        else mostraDomanda();
    }, 2500);
}

function mostraRisultato() {
    quizIntro.style.display = "none";
    quizDomanda.style.display = "none";
    quizRisultato.style.display = "block";
    quizRisultatoPunteggio.innerHTML = punti + "/" + NUMERO_DOMANDE + " PUNTI";
    if (punti < 5) {
        quizRisultatoMessaggio.innerHTML = "Puoi fare di meglio: vai, scopri la biodiversità umbra e torna a fare il quiz!";
        quizRisultatoImmagine.src = "img/gameover.png";
        riproduci("snd/gameover.mp3");
    } else if (punti < 8) {
        quizRisultatoMessaggio.innerHTML = "Bene, ma puoi ancora migliorare!";
        quizRisultatoImmagine.src = "img/intermedio.png";
        riproduci("snd/intermedio.mp3");
    } else {
        quizRisultatoMessaggio.innerHTML = "Ottimo! Conosci la biodiversità umbra come le tue tasche!";
        quizRisultatoImmagine.src = "img/vittoria.png";
        riproduci("snd/victory.mp3");
    }
}

function tornaAllaHome() {
    nascondiTutto();
    cerca.style.display = "block";
    fogliolina.style.display = "block";
}

function onDeviceReady() {
    // Cordova is now initialized. Have fun!

    console.log('Running cordova-' + cordova.platformId + '@' + cordova.version);
    //document.getElementById('deviceready').classList.add('ready');

    // Fix for iOS, should not overlap the top bar
    if (device && device.platform && (device.platform.startsWith("iPhone") || device.platform.startsWith("iOS"))) {
        var body = document.getElementsByTagName("body")[0];
        var div = document.createElement("div");
        div.style.height = "36px";
        div.style.width = "100%";
        div.style.backgroundColor = "white";
        div.classList.add("fixed-top");
        var nav = document.getElementsByTagName("nav")[0];
        nav.style.marginTop = "36px";
        body.prepend(div);
    }

    bottoneScopri.addEventListener("click", function () {
        // Trevi
        // var lat = 42.893333;
        // var lon = 12.761667;
        nascondiTutto();
        fogliolina.style.display = "block";
        caricamento.style.display = "block";
        navigator.geolocation.getCurrentPosition(function (position) {
            cercaBiodiversita(position.coords.latitude, position.coords.longitude);
        }, function () {
            nascondiTutto();
            erroregps.style.display = "block";
            bottoneIndietro.style.display = "block";
        });
    });

    bottoneQuiz.addEventListener("click", function () {
        nascondiTutto();
        bottoneIndietro.style.display = "block";
        quizIntro.style.display = "block";
        quizDomanda.style.display = "none";
        quizRisultato.style.display = "none";
        quiz.style.display = "block";
    });

    bottoneIndietro.addEventListener("click", function () {
        tornaAllaHome();
    });

    informazioni.addEventListener("click", function () {
        nascondiTutto();
        about.style.display = "block";
        bottoneIndietro.style.display = "block";
    });

    bottoneQuizFacile.addEventListener("click", function () {
        iniziaQuiz(FACILE);
    });

    bottoneQuizIntermedio.addEventListener("click", function () {
        iniziaQuiz(INTERMEDIO);
    });

    bottoneQuizDifficile.addEventListener("click", function () {
        iniziaQuiz(DIFFICILE);
    });

    bottoneQuizRisposta1.addEventListener("click", function () {
        mostraRisposta(bottoneQuizRisposta1.innerHTML);
    });

    bottoneQuizRisposta2.addEventListener("click", function () {
        mostraRisposta(bottoneQuizRisposta2.innerHTML);
    });

    bottoneQuizRisposta3.addEventListener("click", function () {
        mostraRisposta(bottoneQuizRisposta3.innerHTML);
    });

    bottoneFineQuiz.addEventListener("click", function () {
        tornaAllaHome();
    });
}