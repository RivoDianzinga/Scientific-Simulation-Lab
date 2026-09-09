BEGIN;

ALTER TABLE simulations
DROP CONSTRAINT simulations_n_points_check;

ALTER TABLE simulations
ADD CONSTRAINT simulations_n_points_check
CHECK (n_points >= 3);

COMMIT;