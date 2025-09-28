import requests
import os
import xml.etree.ElementTree as ET

# GeoServer connection details
GEOSERVER_URL = "http://geoserver:8080/geoserver/rest"
GEOSERVER_USER = "admin"
GEOSERVER_PASS = "geoserver"

# Workspace details
WORKSPACE = "chad"

# Shapefile directories
SHAPEFILE_DIRS = [
    "admin_regions",
    "water_bodies",
    "land_cover",
    "climate_zones"
]

def workspace_exists():
    """Checks if the workspace exists."""
    url = f"{GEOSERVER_URL}/workspaces/{WORKSPACE}"
    response = requests.get(url, auth=(GEOSERVER_USER, GEOSERVER_PASS))
    return response.status_code == 200

def create_workspace():
    """Creates a new workspace in GeoServer if it doesn't exist."""
    if workspace_exists():
        print(f"Workspace '{WORKSPACE}' already exists.")
        return

    url = f"{GEOSERVER_URL}/workspaces"
    headers = {"Content-type": "text/xml"}
    data = f"<workspace><name>{WORKSPACE}</name></workspace>"
    response = requests.post(url, auth=(GEOSERVER_USER, GEOSERVER_PASS), headers=headers, data=data)
    if response.status_code == 201:
        print(f"Workspace '{WORKSPACE}' created successfully.")
    elif response.status_code == 401:
        print("Error: Unauthorized. Check GeoServer credentials.")
    else:
        print(f"Error creating workspace: {response.text}")

def publish_layers():
    """Publishes layers from shapefiles."""
    for dir_name in SHAPEFILE_DIRS:
        store_name = dir_name
        shapefile_path = f"/opt/geoserver_data/data/shapefiles/{dir_name}"

        # Create the data store
        url = f"{GEOSERVER_URL}/workspaces/{WORKSPACE}/datastores"
        headers = {"Content-type": "application/xml"}
        data = f"""
        <dataStore>
            <name>{store_name}</name>
            <connectionParameters>
                <entry key="url">file:{shapefile_path}</entry>
                <entry key="namespace">{WORKSPACE}</entry>
            </connectionParameters>
        </dataStore>
        """
        response = requests.post(url, auth=(GEOSERVER_USER, GEOSERVER_PASS), headers=headers, data=data)
        if response.status_code == 201:
            print(f"Data store '{store_name}' created successfully.")
        else:
            print(f"Error creating data store '{store_name}': {response.text}")
            # Check if it already exists
            if "already exists" in response.text:
                 print(f"Data store '{store_name}' already exists. Continuing...")
            else:
                continue

        # Publish the layers from the data store
        url = f"{GEOSERVER_URL}/workspaces/{WORKSPACE}/datastores/{store_name}/featuretypes.xml"
        response = requests.get(url, auth=(GEOSERVER_USER, GEOSERVER_PASS))
        
        if response.status_code != 200:
            print(f"Error getting feature types for store '{store_name}': {response.text}")
            continue

        try:
            root = ET.fromstring(response.content)
            feature_types = [ft.find('name').text for ft in root.findall('featureType')]
        except ET.ParseError as e:
            print(f"Error parsing XML for store '{store_name}': {e}")
            print(f"Response content: {response.text}")
            continue

        for layer_name in feature_types:
            # Check if layer already exists
            layer_check_url = f"{GEOSERVER_URL}/layers/{WORKSPACE}:{layer_name}"
            layer_response = requests.get(layer_check_url, auth=(GEOSERVER_USER, GEOSERVER_PASS))
            if layer_response.status_code == 200:
                print(f"Layer '{layer_name}' already exists.")
                continue

            publish_url = f"{GEOSERVER_URL}/workspaces/{WORKSPACE}/datastores/{store_name}/featuretypes"
            publish_data = f"<featureType><name>{layer_name}</name></featureType>"
            publish_headers = {"Content-type": "text/xml"}
            publish_response = requests.post(publish_url, auth=(GEOSERVER_USER, GEOSERVER_PASS), headers=publish_headers, data=publish_data)
            
            if publish_response.status_code == 201:
                print(f"Layer '{layer_name}' published successfully.")
            else:
                print(f"Error publishing layer '{layer_name}': {publish_response.text}")


if __name__ == "__main__":
    create_workspace()
    publish_layers()
