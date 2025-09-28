import requests
import os

# GeoServer connection details
GEOSERVER_URL = "http://localhost:8080/geoserver/rest"
GEOSERVER_USER = "admin"
GEOSERVER_PASS = "geoserver"

# Workspace and data store details
WORKSPACE = "sahel"
PG_STORE = "postgis_db"
DB_NAME = "geodb"
DB_HOST = "postgres"
DB_USER = "geouser"
DB_PASS = "geopass"

def create_workspace():
    """Creates the 'sahel' workspace if it doesn't exist."""
    url = f"{GEOSERVER_URL}/workspaces/{WORKSPACE}"
    response = requests.get(url, auth=(GEOSERVER_USER, GEOSERVER_PASS))
    if response.status_code == 200:
        print(f"Workspace '{WORKSPACE}' already exists.")
        return True

    url = f"{GEOSERVER_URL}/workspaces"
    headers = {"Content-type": "text/xml"}
    data = f"<workspace><name>{WORKSPACE}</name></workspace>"
    response = requests.post(url, auth=(GEOSERVER_USER, GEOSERVER_PASS), headers=headers, data=data)
    if response.status_code == 201:
        print(f"Workspace '{WORKSPACE}' created successfully.")
        return True
    else:
        print(f"Error creating workspace '{WORKSPACE}': {response.text}")
        return False

def create_postgis_datastore():
    """Creates a PostGIS data store."""
    url = f"{GEOSERVER_URL}/workspaces/{WORKSPACE}/datastores"
    
    # Check if datastore already exists
    ds_url = f"{url}/{PG_STORE}"
    response = requests.get(ds_url, auth=(GEOSERVER_USER, GEOSERVER_PASS))
    if response.status_code == 200:
        print(f"Data store '{PG_STORE}' already exists.")
        return True

    headers = {"Content-type": "application/xml"}
    data = f"""
    <dataStore>
        <name>{PG_STORE}</name>
        <connectionParameters>
            <host>{DB_HOST}</host>
            <port>5432</port>
            <database>{DB_NAME}</database>
            <user>{DB_USER}</user>
            <passwd>{DB_PASS}</passwd>
            <dbtype>postgis</dbtype>
            <schema>public</schema>
        </connectionParameters>
    </dataStore>
    """
    response = requests.post(url, auth=(GEOSERVER_USER, GEOSERVER_PASS), headers=headers, data=data)
    if response.status_code == 201:
        print(f"Data store '{PG_STORE}' created successfully.")
        return True
    else:
        print(f"Error creating data store '{PG_STORE}': {response.text}")
        return False

def publish_filtered_layer(layer_name, cql_filter):
    """Publishes a layer from the 'spatial_data' table with a CQL filter."""
    
    # First, ensure the feature type is up-to-date
    ft_reload_url = f"{GEOSERVER_URL}/workspaces/{WORKSPACE}/datastores/{PG_STORE}/featuretypes/spatial_data.xml"
    reload_headers = {"Content-type": "application/xml"}
    reload_data = "<featureType><name>spatial_data</name><enabled>true</enabled></featureType>"
    requests.put(ft_reload_url, auth=(GEOSERVER_USER, GEOSERVER_PASS), headers=reload_headers, data=reload_data)


    feature_type_url = f"{GEOSERVER_URL}/workspaces/{WORKSPACE}/datastores/{PG_STORE}/featuretypes"
    
    # Check if layer already exists
    layer_check_url = f"{GEOSERVER_URL}/layers/{WORKSPACE}:{layer_name}"
    layer_response = requests.get(layer_check_url, auth=(GEOSERVER_USER, GEOSERVER_PASS))
    if layer_response.status_code == 200:
        print(f"Layer '{layer_name}' already exists.")
        return

    headers = {"Content-type": "application/xml"}
    data = f"""
    <featureType>
      <name>{layer_name}</name>
      <nativeName>spatial_data</nativeName>
      <cqlFilter>{cql_filter}</cqlFilter>
    </featureType>
    """
    response = requests.post(feature_type_url, auth=(GEOSERVER_USER, GEOSERVER_PASS), headers=headers, data=data)
    if response.status_code == 201:
        print(f"Layer '{layer_name}' published successfully.")
    else:
        print(f"Error publishing layer '{layer_name}': {response.text}")

if __name__ == "__main__":
    if create_workspace():
        if create_postgis_datastore():
            publish_filtered_layer("wells", "type = 'well'")
            publish_filtered_layer("boreholes", "type = 'borehole'")
            publish_filtered_layer("ponds", "type = 'pond'")
