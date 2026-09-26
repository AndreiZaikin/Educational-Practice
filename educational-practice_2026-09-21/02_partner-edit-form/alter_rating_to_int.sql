-- Приведение partners.rating к целому неотрицательному числу.

ALTER TABLE partners
    ALTER COLUMN rating TYPE INT
    USING ROUND(rating)::INT;

ALTER TABLE partners
    ADD CONSTRAINT chk_partners_rating_non_negative
        CHECK (rating IS NULL OR rating >= 0);