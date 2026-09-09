"""
Ici, l'objectif n'est pas de faire du CRUD artificiellement. 
Une campagne va répondre à un vrai besoin scientifique : 
lancer un ensemble de simulations avec un paramètre fixé, 
par rapport aux autres, afin de voir et mème visualiser 
l'influence de ce paramètre.
Les fonctions ici suivent le mème schéma : 
a) connection avec get_connection et .cursor()
b) remplit la base de données avec cursor.execute(commande SQL)
c) cursor.fetch renvoie les données dans rows
d) fermeture de la connexion avec .close()
"""

from database.connection import get_connection

# Ici, on crée une campagne
def create_campaign(
    name: str,
    description: str | None = None,
):
    conn = get_connection() # crée un objet de connexion avec PostgreSQL
    cursor = conn.cursor() # crée un outil permettant d'envoyer du SQL

    try:
        cursor.execute(
            """
            INSERT INTO campaigns (
                name,
                description
            )
            VALUES (%s, %s)
            RETURNING
                id,
                name,
                description,
                created_at;
            """,
            (
                name,
                description,
            ),
        ) # envoie INSERT pour créer une campagne de simulation à PostgreSQL
         # %s ---> paramètres sécurisés
         # RETURNING ---> récupère la ligne créée
        row = cursor.fetchone()

        conn.commit() # valide

        return {
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "created_at": row[3],
        }

    except Exception:
        conn.rollback() # annule su problème
        raise

    finally:
        cursor.close()
        conn.close()

# Ici, on définit la fonction qui fait la lecture de toutes les 
# campagnes. Autrement dit, on consulte toutes les campagnes.
def get_all_campaigns():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT
                id,
                name,
                description,
                created_at
            FROM campaigns
            ORDER BY created_at DESC;
            """
        )
        rows = cursor.fetchall() # récupère toutes les lignes de simulations
        return [
            {
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "created_at": row[3],
            }
            for row in rows
        ]
    finally:
        cursor.close()
        conn.close()

# Ici, on définit une fonction qui permet de récupérer une campagne
# pas son ID. Cela permet de distinguer si :
# la campagne est inexistante ---> erreur 404
# is la campagne existe mais sans simulation ---> [] (vecteur vide)
def get_campaign_by_id(campaign_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT
                id,
                name,
                description,
                created_at
            FROM campaigns
            WHERE id = %s;
            """,
            (campaign_id,),
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return {
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "created_at": row[3],
        }
    finally:
        cursor.close()
        conn.close()

# Ici, on définit la fonction qui supprime une campagne par son id, 
# sans supprimer ses simulations et leurs résultats
def delete_campaign_by_id(campaign_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            DELETE FROM campaigns
            WHERE id = %s
            RETURNING id;
            """,
            (campaign_id,),
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