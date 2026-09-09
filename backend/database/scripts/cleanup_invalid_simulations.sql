BEGIN;
-- Voir d'abord les simulations physiquement / numériquement invalides
SELECT
    id,
    epsilon,
    sigma,
    r_min,
    r_max,
    n_points
FROM simulations
WHERE
       epsilon <= 0
    OR sigma <= 0
    OR r_min <= 0
    OR r_max <= r_min
    OR n_points < 3
    OR r_min >= POWER(2.0, 1.0 / 6.0) * sigma
    OR r_max <= POWER(2.0, 1.0 / 6.0) * sigma
ORDER BY id;
--- Ensuite les supprimer
DELETE FROM simulations
WHERE
       epsilon <= 0
    OR sigma <= 0
    OR r_min <= 0
    OR r_max <= r_min
    OR n_points < 3
    OR r_min >= POWER(2.0, 1.0 / 6.0) * sigma
    OR r_max <= POWER(2.0, 1.0 / 6.0) * sigma
RETURNING id;

COMMIT;