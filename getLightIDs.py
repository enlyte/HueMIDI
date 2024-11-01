import requests
from dotenv import load_dotenv
import os

load_dotenv()

# Retrieve bridge IP and username from environment variables
bridge_ip = os.getenv("BRIDGE_IP")
username = os.getenv("USERNAME")

# Check if variables are loaded
print("Bridge IP:", bridge_ip)
print("Username:", username)

def get_lights():
    url = f"http://{bridge_ip}/api/{username}/lights"
    response = requests.get(url)
    
    # Check if the response was successful
    if response.status_code == 200:
        lights = response.json()

        # Check if lights is a dictionary or a list
        if isinstance(lights, dict):
            for light_id, light_info in lights.items():
                print(f"Light ID: {light_id}, Name: {light_info['name']}")
        elif isinstance(lights, list):
            for light in lights:
                print(f"Light ID: {light.get('id', 'Unknown')}, Name: {light.get('name', 'Unknown')}")
        else:
            print("Unexpected format in response:", lights)

        return lights
    else:
        print("Failed to retrieve lights:", response.status_code, response.text)
        return None

# Call the function
get_lights()
