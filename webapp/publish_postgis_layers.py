import requests
import os
import time

# Give GeoServer time to start up
print("Waiting for GeoServer to start...")
time.sleep(30)
print("Continuing with script.")

# GeoServer connection details
GEOSERVER_URL = "http://geoserver:8080/geoserver/rest"
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

def delete_datastore():
    """Deletes the PostGIS data store if it exists."""
    url = f"{GEOSERVER_URL}/workspaces/{WORKSPACE}/datastores/{PG_STORE}?recurse=true"
    response = requests.delete(url, auth=(GEOSERVER_USER, GEOSERVER_PASS))
    if response.status_code == 200:
        print(f"Data store '{PG_STORE}' deleted successfully.")
        # Wait a bit for GeoServer to process the deletion
        time.sleep(5)
        return True
    elif response.status_code == 404:
        print(f"Data store '{PG_STORE}' does not exist, no need to delete.")
        return True
    else:
        print(f"Error deleting data store '{PG_STORE}': {response.status_code} {response.text}")
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
    feature_type_url = f"{GEOSERVER_URL}/workspaces/{WORKSPACE}/datastores/{PG_STORE}/featuretypes"
    
    # Check if layer already exists
    layer_check_url = f"{GEOSERVER_URL}/layers/{WORKSPACE}:{layer_name}"
    layer_response = requests.get(layer_check_url, auth=(GEOSERVER_USER, GEOSERVER_PASS))
    if layer_response.status_code == 200:
        print(f"Layer '{layer_name}' already exists.")
        # If it exists, we'll remove it to ensure it's recreated with the correct schema
        delete_url = f"{GEOSERVER_URL}/layers/{WORKSPACE}:{layer_name}"
        delete_response = requests.delete(delete_url, auth=(GEOSERVER_USER, GEOSERVER_PASS))
        if delete_response.status_code == 200:
            print(f"Existing layer '{layer_name}' deleted.")
            # Also delete the associated feature type
            ft_delete_url = f"{GEOSERVER_URL}/workspaces/{WORKSPACE}/datastores/{PG_STORE}/featuretypes/{layer_name}"
            ft_delete_response = requests.delete(ft_delete_url, auth=(GEOSERVER_USER, GEOSERVER_PASS))
            if ft_delete_response.status_code == 200:
                print(f"Feature type '{layer_name}' deleted.")
            else:
                print(f"Warning: could not delete feature type '{layer_name}': {ft_delete_response.text}")
        else:
            print(f"Warning: could not delete existing layer '{layer_name}': {delete_response.text}")

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
        # Delete the datastore first to force a refresh of the schema
        if delete_datastore():
            if create_postgis_datastore():
                # A short delay to ensure datastore is ready
                time.sleep(5)
                publish_filtered_layer("wells", "type = 'well'")
                publish_filtered_layer("boreholes", "type = 'borehole'")
                publish_filtered_layer("ponds", "type = 'pond'")
