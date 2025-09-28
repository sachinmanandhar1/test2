#!/bin/bash

if [ ! -f /opt/geoserver_data/initialized.txt ]; then
  echo "Initializing GeoServer settings..."
  
  # Wait for GeoServer to be ready
  while ! curl -s http://localhost:8080/geoserver >/dev/null; do
    echo "Waiting for GeoServer..."
    sleep 5
  done
  
  # Update GeoServer settings
  curl -v -u admin:geoserver -H "Content-type: application/json" -X PUT -d '{"settings": {"proxyBaseUrl": "http://localhost:8080/geoserver"}}' http://localhost:8080/geoserver/rest/settings.json
  
  touch /opt/geoserver_data/initialized.txt
fi