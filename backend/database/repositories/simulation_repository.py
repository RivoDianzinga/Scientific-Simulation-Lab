"""
Ici, on demande à python d'ouvrir une connexion à PostgreSQL, 
et que Python écrive lui-mème dans PostgreSQL. Autrement dit, 
plus aucun INSERT tapé manuellement dans PostgreSQL. 
Python exécute les calculs, ensuite envoie les résultats
d'une simulation dans une base de données sur PostgreSQL.
Une autre fonction permet de sauvegarder toutes les simulations
d'une campagne.
Les fonctions ici suivent le mème schéma : 
a) connection avec get_connection et .cursor()
b) remplit la base de données avec cursor.execute(commande SQL)
c) cursor.fetch renvoie les données dans rows
d) fermeture de la connexion avec .close()
"""
from database.connection import get_connection

# La fonction prend en arguments les paramètres input (epsilon, 
# sigma, r_min, r_max, _npoints) et les paramètres de sortie 
# (distance_equilibre, energie_minimale), ainsi que le id de la 
# campagne. Cette fonction se veut de récupérer tous les inputs 
# et output de toute une campagne. Cette fonction retourne 
# le id de la simulation et le id du résultat.
def save_simulation_with_result(
    epsilon: float,
    sigma: float,
    r_min: float,
    r_max: float,
    n_points: int,
    distance_equilibre: float,
    energie_minimale: float,
    campaign_id: int | None = None,
):
    conn = get_connection() # crée un objet de connexion avec PostgreSQL
    cursor = conn.cursor() # crée un outil permettant d'envoyer du SQL
    try:
        cursor.execute(
            """
            INSERT INTO simulations (
                campaign_id,
                epsilon,
                sigma,
                r_min,
                r_max,
                n_points
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id; 
            """,
            (
                campaign_id,
                epsilon,
                sigma,
                r_min,
                r_max,
                n_points,
            ),
        ) # envoie INSERT des inputs à PostgreSQL
        simulation_id = cursor.fetchone()[0] # récupère le id de la simulation généré
        cursor.execute(
            """
            INSERT INTO results (
                simulation_id,
                equilibrium_distance,
                minimum_energy
            )
            VALUES (%s, %s, %s)
            RETURNING id;
            """,
            (
                simulation_id,
                distance_equilibre,
                energie_minimale,
            ),
        ) # envoie INSERT des output à PostgreSQL
        result_id = cursor.fetchone()[0] # récupère le id du résultat généré
        conn.commit() # valide définitivement l'insertion
        return {
            "simulation_id": simulation_id,
            "result_id": result_id,
        } # rentourne le id de la simulation et le id du résultat

    except Exception:
        conn.rollback() # annule les modifications si quelque chose lors de l'INSERT a échoué
        raise

    finally:
        cursor.close() # ferme le curseur 
        conn.close() # ferme la connexion

# Ici, on ajoute une nouvelle fonction qui va afficher toutes les 
# simulations déjà effectuées. Cette fonction se veut l'historique
# des simulations. Cette fonction fait le "GET", "READ" ou "SELECT"
def get_all_simulations():
    conn = get_connection() # crée un objet de connexion avec PostgreSQL
    cursor = conn.cursor() # crée un outil permettant d'envoyer du SQL
    try:
        cursor.execute(
            """
            SELECT
                s.id,
                s.campaign_id,
                c.name,
                s.epsilon,
                s.sigma,
                s.r_min,
                s.r_max,
                s.n_points,
                s.created_at,
                r.equilibrium_distance,
                r.minimum_energy
            FROM simulations AS s
            LEFT JOIN campaigns AS c 
                ON s.campaign_id = c.id
            LEFT JOIN results AS r
                ON r.simulation_id = s.id
            ORDER BY s.created_at DESC;
            """
        ) # envoie SELECT des input/output à PostgreSQL
        # JOIN --> relie les tables
        # ORDER BY --> trie les simulations
        # LEFT JOIN --> montre-moi quand même la simulation, même si elle n’a pas de campagne
        rows = cursor.fetchall() # récupère toutes les lignes
        return [
            {
                "id": row[0],
                "campaign_id": row[1],
                "campaign_name": row[2],
                "epsilon": row[3],
                "sigma": row[4],
                "r_min": row[5],
                "r_max": row[6],
                "n_points": row[7],
                "created_at": row[8],
                "distance_equilibre": row[9],
                "energie_minimale": row[10],
            }
            for row in rows
        ] # retourne les input/output
    finally:
        cursor.close()
        conn.close()

# Ici, on rajoute une fonction qui pourra récupérer une simulation
# pas son id
def get_simulation_by_id(simulation_id: int):
    conn = get_connection() # crée un objet de connexion avec PostgreSQL
    cursor = conn.cursor() # crée un outil permettant d'envoyer du SQL
    try:
        cursor.execute(
            """
            SELECT
                s.id,
                s.campaign_id,
                c.name,
                s.epsilon,
                s.sigma,
                s.r_min,
                s.r_max,
                s.n_points,
                s.created_at,
                r.equilibrium_distance,
                r.minimum_energy
            FROM simulations AS s
            LEFT JOIN campaigns AS c
                ON s.campaign_id = c.id
            LEFT JOIN results AS r
                ON r.simulation_id = s.id
            WHERE s.id = %s;
            """,
            (simulation_id,),
        ) # envoie SELECT des input/output du id de la simulation sélectionnée à PostgreSQL
        row = cursor.fetchone() # cherche une seule simulation
        if row is None:
            return None
        return {
            "id": row[0],
            "campaign_id": row[1],
            "campaign_name": row[2],
            "epsilon": row[3],
            "sigma": row[4],
            "r_min": row[5],
            "r_max": row[6],
            "n_points": row[7],
            "created_at": row[8],
            "distance_equilibre": row[9],
            "energie_minimale": row[10],
        } # retourne les input/output de la simulation sélectionnée
    finally:
        cursor.close()
        conn.close()

# Ici, on définit une fonction qui récupérer les simulations d'une 
# campagne
def get_simulations_by_campaign_id(campaign_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT
                s.id,
                s.campaign_id,
                c.name,
                s.epsilon,
                s.sigma,
                s.r_min,
                s.r_max,
                s.n_points,
                s.created_at,
                r.equilibrium_distance,
                r.minimum_energy
            FROM simulations AS s

            JOIN campaigns AS c
                ON s.campaign_id = c.id

            LEFT JOIN results AS r
                ON r.simulation_id = s.id

            WHERE s.campaign_id = %s

            ORDER BY s.created_at ASC;
            """,
            (campaign_id,),
        )

        rows = cursor.fetchall()

        return [
            {
                "id": row[0],
                "campaign_id": row[1],
                "campaign_name": row[2],
                "epsilon": row[3],
                "sigma": row[4],
                "r_min": row[5],
                "r_max": row[6],
                "n_points": row[7],
                "created_at": row[8],
                # vocabulaire exposé par ton API
                "distance_equilibre": row[9],
                "energie_minimale": row[10],
            }
            for row in rows
        ]
    finally:
        cursor.close()
        conn.close()

# Ici, on supprime une simulation par son id
def delete_simulation_by_id(simulation_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            DELETE FROM simulations
            WHERE id = %s
            RETURNING id;
            """,
            (simulation_id,),
        )
        row = cursor.fetchone()
        conn.commit()
        return row is not None
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()