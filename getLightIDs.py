# getLightIDs.py
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
        for light_id, light_info in lights.items():
            print(f"Light ID: {light_id}, Name: {light_info['name']}")
        return lights
    else:
        print("Failed to retrieve lights:", response.status_code, response.text)
        return None

# Call the function
get_lights()
