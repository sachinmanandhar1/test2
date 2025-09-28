CREATE EXTENSION IF NOT EXISTS postgis;
CREATE TABLE public.spatial_data (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    geom GEOMETRY(GEOMETRY, 4326)
);
INSERT INTO spatial_data (name, geom) VALUES (
    'Sample Point',
    ST_GeomFromText('POINT(-74.006 40.7128)', 4326)
);