--- Creation de notre base de données
--- Les objets métiers sont les campagnes (campaigns), 
--- les simulations (simulations)
--- et les résultats (results)
--- Une campagne comprend son identifiant, un nom court
--- une description détaillée et le temps de création
--- Une simulation comprend les paramètres de calcul
--- Un résultat comprend les résultats
--- Une campagne comprendre plusieurs simulations
--- et une simulation n'a qu'un seul résultat 
/*
┌─────────────────────┐
│      CAMPAIGN       │
├─────────────────────┤
│ id                  │
│ name                │
│ description         │
│ created_at          │
└──────────┬──────────┘
           │
         (0,N)
           │
        CONTIENT
           │
         (0,1)
           │
┌──────────▼──────────┐
│     SIMULATION      │
├─────────────────────┤
│ id                  │
│ epsilon             │
│ sigma               │
│ r_min               │
│ r_max               │
│ n_points            │
│ created_at          │
└──────────┬──────────┘
           │
         (0,1)
           │
         PRODUIT
           │
         (1,1)
           │
┌──────────▼──────────┐
│       RESULT        │
├─────────────────────┤
│ id                  │
│ equilibrium_distance│
│ minimum_energy      │
└─────────────────────┘
*/

--- Crée la table des campagnes
CREATE TABLE campaigns (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP
);

--- Crée la table des simulations
--- sa clé étrangère est campaign_id
--- une campagne peut-ètre annulée mais ses simulations
--- restent disponibles ---> ON DELETE SET NULL
CREATE TABLE simulations (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    campaign_id INTEGER,
    epsilon DOUBLE PRECISION NOT NULL
        CHECK (epsilon > 0),
    sigma DOUBLE PRECISION NOT NULL
        CHECK (sigma > 0),
    r_min DOUBLE PRECISION NOT NULL
        CHECK (r_min > 0),
    r_max DOUBLE PRECISION NOT NULL,
    n_points INTEGER NOT NULL
        CHECK (n_points >= 3),
    created_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT check_distance_range
        CHECK (r_max > r_min),
    CONSTRAINT fk_simulation_campaign
        FOREIGN KEY (campaign_id)
        REFERENCES campaigns(id)
        ON DELETE SET NULL
);

--- Crée la table des résultats
--- sa clé étrangère est simulation_id
--- une simulation peut ètre annulée, ainsi que tous ses résultats
--- ---> ON DELETE CASCADE 
CREATE TABLE results (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    simulation_id INTEGER NOT NULL UNIQUE,
    equilibrium_distance DOUBLE PRECISION NOT NULL
        CHECK (equilibrium_distance > 0),
    minimum_energy DOUBLE PRECISION NOT NULL,
    CONSTRAINT fk_result_simulation
        FOREIGN KEY (simulation_id)
        REFERENCES simulations(id)
        ON DELETE CASCADE
);