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

var bottoneScopri = document.getElementById("bottone-scopri");
var cerca = document.getElementById("cerca");
var risultati = document.getElementById("risultati");
var fogliolina = document.getElementById("fogliolina");
var bottoneIndietro = document.getElementById("bottone-indietro");
var informazioni = document.getElementById("informazioni");
var about = document.getElementById("about");
var erroregps = document.getElementById("erroregps");
var caricamento = document.getElementById("caricamento");

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
    if (found.length > 0) {
        console.log("FOUND!", found.length)
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

function onDeviceReady() {
    // Cordova is now initialized. Have fun!

    console.log('Running cordova-' + cordova.platformId + '@' + cordova.version);
    //document.getElementById('deviceready').classList.add('ready');

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

    bottoneIndietro.addEventListener("click", function () {
        nascondiTutto();
        cerca.style.display = "block";
        fogliolina.style.display = "block";
    });

    informazioni.addEventListener("click", function () {
        nascondiTutto();
        about.style.display = "block";
        bottoneIndietro.style.display = "block";
    });
}
