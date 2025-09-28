Key Integration Steps
-----------------------------
GeoServer to PostGIS:

Access GeoServer at http://localhost:8080/geoserver (admin/geoserver).

Add a new PostGIS data store using:

Host: postgres (Docker service name)

Database: geodb

User: geouser

Password: geopass

Publish layers from the spatial_data table.

Web Application:
--------------------
Ensure your Java EE app uses:

PrimeFaces for UI components.

OpenLayers to display maps from GeoServer WMS/WFS.

Example OpenLayers integration:
--------------------------------
javascript
var map = new ol.Map({
  target: 'map',
  layers: [
    new ol.layer.Tile({
      source: new ol.source.OSM()
    }),
    new ol.layer.Tile({
      source: new ol.source.TileWMS({
        url: 'http://localhost:8080/geoserver/wms',
        params: { 'LAYERS': 'workspace:layer_name' }
      })
    })
  ],
  view: new ol.View({
    center: ol.proj.fromLonLat([-74.006, 40.7128]),
    zoom: 10
  })
});

Run the Stack
----------------
bash
docker-compose up -d
Validation
PostgreSQL: Connect via psql -h localhost -U geouser -d geodb.

GeoServer: Access http://localhost:8080/geoserver.

Web App: Access http://localhost:8080 to test PrimeFaces/OpenLayers integration.

This setup ensures all components are linked, with GeoServer serving spatial data from PostGIS and the web app consuming it via OpenLayers. Adjust versions/ports as needed.

