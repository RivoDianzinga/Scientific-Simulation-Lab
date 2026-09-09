/*
Ici on teste, on manipule les tables denotre base de données
scientific_simulation_lab
*/
-- =====================================================
-- TEST 1 : CHECK epsilon > 0
-- =====================================================

INSERT INTO simulations (
    campaign_id,
    epsilon,
    sigma,
    r_min,
    r_max,
    n_points
)
VALUES (
    1,
    -1.0,
    1.0,
    0.8,
    3.0,
    500
);


-- =====================================================
-- TEST 2 : FOREIGN KEY campaign_id
-- =====================================================

INSERT INTO simulations (
    campaign_id,
    epsilon,
    sigma,
    r_min,
    r_max,
    n_points
)
VALUES (
    999,
    1.0,
    1.0,
    0.8,
    3.0,
    500
);


-- =====================================================
-- TEST 3 : NOT NULL sigma
-- =====================================================

INSERT INTO simulations (
    campaign_id,
    epsilon,
    sigma,
    r_min,
    r_max,
    n_points
)
VALUES (
    1,
    1.0,
    NULL,
    0.8,
    3.0,
    500
);