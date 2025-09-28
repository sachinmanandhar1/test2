CREATE EXTENSION IF NOT EXISTS postgis;
CREATE TABLE public.spatial_data (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    type VARCHAR(50),
    description TEXT,
    geom GEOMETRY(GEOMETRY, 4326)
);
INSERT INTO spatial_data (name, type, description, geom) VALUES (
    'Sample Point',
    'well',
    'This is a sample well.',
    ST_GeomFromText('POINT(-74.006 40.7128)', 4326)
);
-- Add more data for wells, boreholes, and ponds
INSERT INTO spatial_data (name, type, description, geom) VALUES ('Well in Mali', 'well', 'A traditional well in a village near Timbuktu.', ST_GeomFromText('POINT(-3.9962 17.5707)', 4326));
INSERT INTO spatial_data (name, type, description, geom) VALUES ('Well in Niger', 'well', 'A community well in the Agadez region.', ST_GeomFromText('POINT(8.0817 17.6078)', 4326));
INSERT INTO spatial_data (name, type, description, geom) VALUES ('Borehole in Chad', 'borehole', 'A deep borehole providing water for agriculture.', ST_GeomFromText('POINT(18.7322 15.4542)', 4326));
INSERT INTO spatial_data (name, type, description, geom) VALUES ('Borehole in Sudan', 'borehole', 'A borehole with a hand pump.', ST_GeomFromText('POINT(32.525 15.369)', 4326));
INSERT INTO spatial_data (name, type, description, geom) VALUES ('Pond in Nigeria', 'pond', 'A natural pond used for livestock.', ST_GeomFromText('POINT(7.7 11.39)', 4326));
INSERT INTO spatial_data (name, type, description, geom) VALUES ('Seasonal Pond in Mali', 'pond', 'A seasonal pond that fills during the rainy season.', ST_GeomFromText('POINT(-4.5 17.0)', 4326));