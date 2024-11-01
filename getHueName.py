# getHueName.py
import requests
from dotenv import load_dotenv
import os

# Retrieve bridge IP from environment variables
load_dotenv()

def get_username(bridge_ip):
    url = f"http://{bridge_ip}/api"
    payload = {"devicetype": "my_hue_app"}
    response = requests.post(url, json=payload)
    return response.json()

bridge_ip = os.getenv("BRIDGE_IP")
username_response = get_username(bridge_ip)
print(username_response)  # Save the "username" key from this response
