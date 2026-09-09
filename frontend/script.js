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


// Ici, on prépare une fonction Javascript dédiée aux graphiques, 
// en utilisant Plotly.react() qui est utilisé pour mettre à jour 
// intelligemment le graphe existant, c-à-d, il est utilisé 
// lorsqu'il s'agit de modifier souvent les données affichées :
// nouvelle ssimulation, nouvelle campagne, nouvelle sélection
// de courbes, etc.
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
        // récupère le button de simulation
        const submitButton =
            document.getElementById(
                "simulation-submit-button"
            );
        // cherche la valeur id de la campagne
        const campaignValue = document.getElementById("campaign-select").value;
        const campaignId =
            campaignValue === ""
            ? null
            : Number(campaignValue);        
        // lit les paramètres de simulation du formulaire
        // en rajoutant le id de la campagne
        const parametres = {
            epsilon: Number(document.querySelector("#epsilon").value),
            sigma: Number(document.querySelector("#sigma").value),
            r_min: Number(document.querySelector("#r-min").value),
            r_max: Number(document.querySelector("#r-max").value),
            points: Number(document.querySelector("#points").value),
            campaign_id: campaignId 
        };
        //
        submitButton.disabled = true;
        submitButton.textContent = "Calcul en cours...";
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

            if (!reponse.ok) {
                const errorData = await reponse.json();
                throw new Error(
                    errorData.detail ??
                    "Erreur pendant la simulation."
                );
            }

            // met la réponse json dans donnees
            const donnees = await reponse.json();

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
            await chargerHistorique();
        }
        catch (error) {
            console.error(error);
            alert (
                `Erreur : ${error.message}`
            );
        } finally {
            submitButton.disabled = false;
            submitButton.textContent = "Lancer la simulation";
        }
    }
);

// Ici, on définit la fonction qui permet de charger la 
// simulation
async function chargerSimulation(simulationId) {
    try {
        const response = await fetch(
            `${API_BASE_URL}/api/simulations/${simulationId}`
        );

        if (!response.ok) {
            throw new Error(
                "Impossible de charger la simulation."
            );
        }

        const simulation = await response.json();

        document.getElementById("epsilon").value = 
            simulation.epsilon;

        document.getElementById("sigma").value =
            simulation.sigma;

        document.getElementById("r-min").value =
            simulation.r_min;

        document.getElementById("r-max").value =
            simulation.r_max;

        document.getElementById("points").value =
            simulation.n_points;
        
        affichageDistance.textContent =
            simulation.distance_equilibre;
            
        affichageEnergie.textContent =
            simulation.energie_minimale;
            
        afficherGraphiques(simulation);    

        console.log(
            "Simulation rechargée :",
            simulation
        );

    } catch (error) {
        console.error(error);
    }
}

// Ici, on définit la fonction qui affiche l'historique des 
// calculs de simulation
async function chargerHistorique() {
    const listeHistorique =
        document.getElementById("liste-historique");
    try {
        const response = await fetch(
            `${API_BASE_URL}/api/simulations`
        );
        if (!response.ok) {
            throw new Error(
                "Impossible de récupérer l'historique."
            );
        }
        const simulations = await response.json(); // reçoit la réponse en format JSON
        listeHistorique.innerHTML = "";
        if (simulations.length === 0) {
            listeHistorique.innerHTML =
                "<p>Aucune simulation enregistrée.</p>";
            return;
        }
        simulations.forEach((simulation) => { // parcourt les simulations une à une
            const element = document.createElement("div");
            element.classList.add("simulation-history-item");
            element.innerHTML = `
                <h3>Simulation #${simulation.id}</h3>
                <p>
                    ε = ${simulation.epsilon},
                    σ = ${simulation.sigma}
                </p>
                <p>
                    r : ${simulation.r_min}
                    → ${simulation.r_max}
                </p>
                <p>
                    Nombre de points :
                    ${simulation.n_points}
                </p>
                <p>
                    Distance d'équilibre :
                    ${simulation.distance_equilibre}
                </p>
                <p>
                    Énergie minimale :
                    ${simulation.energie_minimale}
                </p>
                <p>
                    Campagne :
                    ${simulation.campaign_name ?? "Aucune"}
                </p>   
                <button 
                    type="button"
                    class="reload-simulation"
                    data-simulation-id="${simulation.id}"
                >
                    Recharger cette simulation
                </button>    
                <button
                    type="button"
                    class="delete-simulation-button"
                    data-id="${simulation.id}"
                >
                    Supprimer
                </button>                 
            `;
            listeHistorique.appendChild(element);
            const reloadButton = element.querySelector(".reload-simulation");
            reloadButton.addEventListener("click", () => {
                const simulationId = 
                    Number(reloadButton.dataset.simulationId);
                chargerSimulation(simulation.id);
            });
            const deleteButton =
                element.querySelector(
                    ".delete-simulation-button"
                );

            deleteButton.addEventListener(
                "click",
                async () => {
                    const simulationId =
                        Number(deleteButton.dataset.id);

                    const confirmation = confirm(
                        `Supprimer la simulation #${simulationId} ?`
                    );

                    if (!confirmation) {
                        return;
                    }

                    try {
                        const response = await fetch(
                            `${API_BASE_URL}/api/simulations/${simulationId}`,
                            {
                                method: "DELETE"
                            }
                        );

                    if (!response.ok) {
                        throw new Error(
                            "Impossible de supprimer la simulation."
                        );
                    }

                    await chargerHistorique();

                } catch (error) {
                    console.error(error);
                    alert(error.message);
                }
            }
        );
    });

    } catch (error) {
        console.error(error);
        listeHistorique.innerHTML =
            `<p>Erreur : ${error.message}</p>`;
    }
}
// Charger l'historique depuis le fronted
document
    .getElementById("charger-historique")
    .addEventListener(
        "click",
        chargerHistorique
    );

// Ici, on charge les campagnes depuis PostgreSQL
async function chargerCampagnes() {
    try {
        const response = await fetch(
            `${API_BASE_URL}/api/campaigns`
        );

        if (!response.ok) {
            throw new Error(
                "Impossible de charger les campagnes."
            );
        }

        const campagnes = await response.json();
        const campaignSelect =
            document.getElementById("campaign-select");

        const comparisonSelect =
            document.getElementById(
            "comparison-campaign-select"
        );

        campaignSelect.innerHTML = `
            <option value="">
            Aucune campagne
            </option>
        `;

        comparisonSelect.innerHTML = `
            <option value="">
            Choisir une campagne
            </option>
        `;

        campagnes.forEach((campagne) => {
            const optionSimulation =
            document.createElement("option");

            optionSimulation.value = campagne.id;
            optionSimulation.textContent = campagne.name;

            campaignSelect.appendChild(optionSimulation);

            const optionComparison =
                document.createElement("option");

            optionComparison.value = campagne.id;
            optionComparison.textContent = campagne.name;

            comparisonSelect.appendChild(optionComparison);
        });

        const select =
            document.getElementById("campaign-select");

        select.innerHTML = `
            <option value="">
                Aucune campagne
            </option>
        `;

        campagnes.forEach((campagne) => {
            const option =
                document.createElement("option");

            option.value = campagne.id;
            option.textContent = campagne.name;

            select.appendChild(option);
        });

    } catch (error) {
        console.error(error);
    }
}

// Lorsqu'on choisit une campagne, récupérer ses simulations
const comparisonCampaignSelect =
    document.getElementById(
        "comparison-campaign-select"
    );

comparisonCampaignSelect.addEventListener(
    "change",
    async () => {
        const campaignId =
            comparisonCampaignSelect.value;

        if (campaignId === "") {
            document.getElementById(
                "campaign-simulations"
            ).innerHTML = "";

            return;
        }

        await chargerSimulationsCampagne(
            Number(campaignId)
        );
    }
);

async function chargerSimulationsCampagne(
    campaignId
) {
    const container =
        document.getElementById(
            "campaign-simulations"
        );

    try {
        const response = await fetch(
            `${API_BASE_URL}/api/campaigns/${campaignId}/simulations`
        );

        if (!response.ok) {
            throw new Error(
                "Impossible de charger la campagne."
            );
        }

        const data = await response.json();

        container.innerHTML = `
            <h3>${data.campaign.name}</h3>

            <p>
                ${data.campaign.description ?? ""}
            </p>
            <button id="delete-campaign-button">
                Supprimer la campagne
            </button>
        `;

        const deleteCampaignButton =
            document.getElementById(
            "delete-campaign-button"
        );

        deleteCampaignButton.addEventListener(
            "click",
            async () => {
                const confirmation = confirm(
                    `Supprimer la campagne "${data.campaign.name}" ?\n\n` +
                    "Les simulations appartenant à cette campagne seront conservées."
                );

                if (!confirmation) {
                    return;
                }

                try {
                    const response = await fetch(
                        `${API_BASE_URL}/api/campaigns/${data.campaign.id}`,
                        {
                            method: "DELETE"
                        }
                    );

                    if (!response.ok) {
                        throw new Error(
                            "Impossible de supprimer la campagne."
                        );
                    }

                    await chargerCampagnes();
                    await chargerHistorique();

                    container.innerHTML = "";

                    document.getElementById(
                        "comparison-campaign-select"
                    ).value = "";

                } catch (error) {
                    console.error(error);
                    alert(error.message);
                }
            }
        );

        if (data.simulations.length === 0) {
            container.innerHTML += `
                <p>
                    Cette campagne ne contient
                    aucune simulation.
                </p>
            `;

            return;
        }

        data.simulations.forEach((simulation) => {
            const element =
                document.createElement("div");

            element.classList.add(
                "comparison-simulation-item"
            );

            element.innerHTML = `
                <label>
                    <input
                        type="checkbox"
                        class="simulation-checkbox"
                        value="${simulation.id}"
                    >

                    Simulation #${simulation.id}

                    — ε = ${simulation.epsilon}

                    — σ = ${simulation.sigma}
                </label>

                <p>
                    Distance d'équilibre :
                    ${simulation.distance_equilibre}
                </p>

                <p>
                    Énergie minimale :
                    ${simulation.energie_minimale}
                </p>
            `;

            container.appendChild(element);
        });

        mettreAJourBoutonComparaison();

        document
            .querySelectorAll(
                ".simulation-checkbox"
            )
            .forEach((checkbox) => {
                checkbox.addEventListener(
                    "change",
                    mettreAJourBoutonComparaison
                );
            });

    } catch (error) {
        console.error(error);

        container.innerHTML = `
            <p>Erreur : ${error.message}</p>
        `;
    }
}

// Ici, la fonction qui active le bouton seulement avec 
// au moins 2 simulations
function mettreAJourBoutonComparaison() {
    const checked =
        document.querySelectorAll(
            ".simulation-checkbox:checked"
        );

    const button =
        document.getElementById(
            "compare-simulations"
        );

    button.disabled = checked.length < 2;
}

// Créer une campagne depuis le frontend
document
    .getElementById("campaign-form")
    .addEventListener(
        "submit",
        async (event) => {
            event.preventDefault();

            const name =
                document
                    .getElementById("campaign-name")
                    .value;

            const description =
                document
                    .getElementById("campaign-description")
                    .value;

            try {
                const response = await fetch(
                    `${API_BASE_URL}/api/campaigns`,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type": "application/json",
                        },

                        body: JSON.stringify({
                            name: name,
                            description: description || null,
                        }),
                    }
                );

                if (!response.ok) {
                    throw new Error(
                        "Impossible de créer la campagne."
                    );
                }

                const campagne =
                    await response.json();

                console.log(
                    "Campagne créée :",
                    campagne
                );

                await chargerCampagnes();

                document
                    .getElementById("campaign-select")
                    .value = campagne.id;

            } catch (error) {
                console.error(error);
            }
        }
    );

// Charger les campagnes au démarrage
chargerCampagnes();

// Ici, on récupère les courbes des simulations sélectionnées
document
    .getElementById("compare-simulations")
    .addEventListener(
        "click",
        comparerSimulationsSelectionnees
    );

async function comparerSimulationsSelectionnees() {
    const checked =
        document.querySelectorAll(
            ".simulation-checkbox:checked"
        );

    const simulationIds =
        Array.from(checked).map(
            (checkbox) => Number(checkbox.value)
        );

    try {
        const simulations =
            await Promise.all(
                simulationIds.map(
                    async (id) => {
                        const response = await fetch(
                            `${API_BASE_URL}/api/simulations/${id}`
                        );

                        if (!response.ok) {
                            throw new Error(
                                `Impossible de charger la simulation ${id}.`
                            );
                        }

                        return response.json();
                    }
                )
            );

        afficherComparaison(simulations);

    } catch (error) {
        console.error(error);
    }
}

// Détection automatique du paramètre constant
function detecterParametreComparaison(simulations) {
    const epsilonValues = new Set(
        simulations.map(
            (simulation) => simulation.epsilon
        )
    );

    const sigmaValues = new Set(
        simulations.map(
            (simulation) => simulation.sigma
        )
    );

    if (
        epsilonValues.size > 1 &&
        sigmaValues.size === 1
    ) {
        return "epsilon";
    }

    if (
        sigmaValues.size > 1 &&
        epsilonValues.size === 1
    ) {
        return "sigma";
    }

    return null;
}

// Superposition réelle des courbes en utilisant Plotly.newplot()
// qui est utilisé pour construire/reconstruire à partir des 
// données qui existent déjà.
function afficherComparaison(simulations) {
    const parametreComparaison =
        detecterParametreComparaison(simulations);

    if (parametreComparaison === null) {
        alert(
            "La comparaison nécessite qu'un seul paramètre varie : epsilon ou sigma."
        );
        return;
    }
    const simulationsTriees = [...simulations].sort(
        (a, b) =>
            a[parametreComparaison] -
            b[parametreComparaison]
    );
    // Graphe 1 - Comparaison de V(r)
    const tracesPotentiel =
        simulationsTriees.map((simulation) => ({
            x: simulation.r,
            y: simulation.potentiel,
            mode: "lines",
            showlegend: true,
            name:
                `${parametreComparaison} = ${simulation[parametreComparaison]}`
        }));

    Plotly.newPlot(
        "comparison-potential-graph",
        tracesPotentiel,
        {
            title: {text: "Comparaison des potentiels V(r)"},

            xaxis: {
                title: {text: "Distance r"}, 
                automargin: true
            },

            yaxis: {
                title: {text: "Potentiel V(r)"},
                automargin: true
            },

            showlegend: true,

            legend: {
                x: 1.02,
                y: 1
            },
            margin: {
                l: 90,
                r: 180,
                b: 80,
                t:80
            }
        }
    );
    // Graphe 2 - Comparaison F(r)  
    const tracesForce =
        simulationsTriees.map((simulation) => ({
            x: simulation.r,
            y: simulation.force_analytique,
            mode: "lines",
            showlegend: true,
            name:
                `${parametreComparaison} = ${simulation[parametreComparaison]}`
        }));

    Plotly.newPlot(
        "comparison-force-graph",
        tracesForce,
        {
            title: {text: "Comparaison des forces interatomiques F(r)"},

            xaxis: {
                title: {text: "Distance r"},
                automargin: true
            },

            yaxis: {
                title: {text: "Force F(r)"},
                automargin: true
            },

            showlegend: true,

            legend: {
                x: 1.02,
                y: 1
            },
            margin: {
                l: 90,
                r: 180,
                b: 80,
                t: 80
            }
        }
    );  
    // Graphe 3 Distance equilibre en fonction du paramètre
    const parametres =
        simulationsTriees.map(
        (simulation) =>
        simulation[parametreComparaison]
        );

    const distancesEquilibre =
        simulationsTriees.map(
        (simulation) =>
        simulation.distance_equilibre
        );

    Plotly.newPlot(
        "comparison-distance-equilibre-graph",
        [
            {
                x: parametres,
                y: distancesEquilibre,
                mode: "lines+markers",
                name: "Distance d'équilibre",
                showlegend: true
            }
        ],
        {
            title: { text: 
                `Distance d'équilibre en fonction de ${parametreComparaison}`},

            xaxis: {
                title: {text: `Paramètre ${parametreComparaison}`},
                automargin: true
            },

            yaxis: {
                title: {text: "Distance d'équilibre R_eq"},
                automargin: true
            },
            showlegend: true,
            legend: {
                x: 1.02,
                y: 1
            },
            margin: {
                l: 110,
                r: 180,
                b: 80,
                t: 80
            }
        }
    );
    // Graphe 4 - energie minimale en fonction du parametre
        const energiesMinimales =
        simulationsTriees.map(
            (simulation) =>
                simulation.energie_minimale
        );

    Plotly.newPlot(
        "comparison-energie-minimale-graph",
        [
            {
                x: parametres,
                y: energiesMinimales,
                mode: "lines+markers",
                name: "Énergie minimale",
                showlegend: true
            }
        ],
        {
            title: {text: 
                `Énergie minimale en fonction de ${parametreComparaison}`},

            xaxis: {
                title: {text: `Paramètre ${parametreComparaison}`},
                automargin: true
            },

            yaxis: {
                title: {text: "Énergie minimale E_min"},
                automargin: true
            },
            showlegend: true,
            legend: {
                x: 1.02,
                y: 1
            },
            margin: {
                l:110,
                r: 180,
                b: 80,
                t: 80
            }
        }
    );
}

// Pour le bouton de retour vers le formulaire
// Référence au bouton de retour
const backToTopButton =
    document.getElementById(
        "back-to-top"
    );

// Faire apparaître ce bouton seulement quand on a 
// suffisamment descendu    
window.addEventListener(
    "scroll",
    () => {
        if (window.scrollY > 500) {
            backToTopButton.style.display =
                "block";
        } else {
            backToTopButton.style.display =
                "none";
        }
    }
);

// Revenir au formulaire de simulation
backToTopButton.addEventListener(
    "click",
    () => {
        document
            .getElementById(
                "form-simulation"
            )
            .scrollIntoView({
                behavior: "smooth",
                block: "start"
            });
    }
);