/* 
Ici, on fait communiquer javascript et python
*/

/*
Ci-dessous, on définit une variable de URL qui déterminera si c'est Render ou c'est
le localhost:3000 qui est utilisé. Cette variable est pratique, plutot que de
commenter et décommenter à chaque fois. 
*/
const API_BASE_URL = 
    window.location.hostname === "localhost" ||
    window.location.hostname === "127.0.0.1"
        ? "http://localhost:8000"
        : "https://scientific-simulation-lab-api.onrender.com";

// On récupère les références des objets HTML pour les 
// transformer en objets javascript
const formSimulation =
    document.querySelector("#form-simulation");

const affichageDistance =
    document.querySelector("#distance-equilibre");

const affichageEnergie =
    document.querySelector("#energie-minimale");


// Ici, on prépare une fonction Javascript dédiée aux graphiques
function afficherGraphiques(donnees) {
    // -----------------------------
    // Graphe du potentiel
    // -----------------------------
    const tracePotentiel = {
        x: donnees.r,
        y: donnees.potentiel,
        type: "scatter",
        mode: "lines",
        name: "V(r)"
    };

    const traceMinimum = {
        x: [donnees.distance_equilibre],
        y: [donnees.energie_minimale],
        type: "scatter",
        mode: "markers",
        name: "Minimum"
    };

    const layoutPotentiel = {

        title: {
            text: "Potentiel de Lennard-Jones"
        },

        xaxis: {
            title: {
                text: "Distance r"
            }
        },

        yaxis: {
            title: {
                text: "Potentiel V(r)"
            }
        }
    };
    // Plotly react est très pratique pour actualiser 
    // plus rapidement les graphiques
    Plotly.react(
        "graph-potentiel",
        [
            tracePotentiel,
            traceMinimum
        ],
        layoutPotentiel,
        {
            responsive: true
        }
    );
    // -----------------------------
    // Graphe des forces
    // -----------------------------
    const traceForceAnalytique = {
        x: donnees.r,
        y: donnees.force_analytique,
        type: "scatter",
        mode: "lines",
        name: "Force analytique"
    };

    const traceForceNumerique = {
        x: donnees.r,
        y: donnees.force_numerique,
        type: "scatter",
        mode: "lines",
        name: "Force numérique",
        line: {
            dash: "dot"
        }
    };

    const layoutForces = {

        title: {
            text: "Forces interatomiques"
        },

        xaxis: {
            title: {
                text: "Distance r"
            }
        },

        yaxis: {
            title: {
                text: "Force F(r)"
            }
        }
    };

    Plotly.react(
        "graph-forces",
        [
            traceForceAnalytique,
            traceForceNumerique
        ],
        layoutForces,
        {
            responsive: true
        }
    );
}    

// Lance à la fois la simulation et la visualisation des graphiques  
// une fois que le bouton "submit" est cliqué
formSimulation.addEventListener("submit", async function (event) {
        event.preventDefault();
        // lit les paramètres de simulation du formulaire
        const parametres = {
            epsilon: Number(document.querySelector("#epsilon").value),
            sigma: Number(document.querySelector("#sigma").value),
            r_min: Number(document.querySelector("#r-min").value),
            r_max: Number(document.querySelector("#r-max").value),
            points: Number(document.querySelector("#points").value)
        };
        // prend la réponde JSON de l'api
        try {
            const reponse = await fetch(
                `${API_BASE_URL}/api/simulations/lennard-jones`,
//                "http://127.0.0.1:8000/api/simulations/lennard-jones",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(parametres)
                }
            );
            // met la réponse json dans donnees
            const donnees = await reponse.json();

            if (!reponse.ok) {
                console.error(donnees);
                return;
            }
            // extrait la distance d'équilibre de donnees pour la 
            // lui attribuer à affichageDistance
            affichageDistance.textContent =
                donnees.distance_equilibre;
            // extrait l'énergie minimale de donnees pour la lui
            // attribuer à affichageEnergie
            affichageEnergie.textContent =
                donnees.energie_minimale;
            // Connecte toute la partie visualisation au calcul lancé
            afficherGraphiques(donnees);
        }
        catch (erreur) {
            console.error(
                "Erreur de communication avec l'API :",
                erreur
            );
        }
    }
);
