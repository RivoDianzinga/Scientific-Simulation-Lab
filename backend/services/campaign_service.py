"""
Ici, on rappelle les fonctions qui permettent de créer et consulter
une campagne
"""

from database.repositories.campaign_repository import (
    create_campaign,
    get_all_campaigns,
    get_campaign_by_id, 
    delete_campaign_by_id
)

from database.repositories.simulation_repository import (
    get_simulations_by_campaign_id
)

# Création d'une nouvelle campagne
def create_new_campaign(
    name: str,
    description: str | None = None,
):
    return create_campaign(
        name=name,
        description=description,
    )

# Lecture/Consultation de toutes les campagnes
def get_campaigns():
    return get_all_campaigns()

# Lecture/Consultation des simulations d'une campagne référencée par
# un id
def get_campaign_simulations(campaign_id: int):
    campaign = get_campaign_by_id(campaign_id)
    if campaign is None:
        return None
    simulations = get_simulations_by_campaign_id(campaign_id)
    return {
        "campaign": campaign,
        "simulations": simulations,
    }

# Ici, on supprime une campagne par son id
def delete_campaign(campaign_id: int) -> bool:
    return delete_campaign_by_id(campaign_id)