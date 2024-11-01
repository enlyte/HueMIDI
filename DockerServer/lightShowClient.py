import requests
import time
import threading
from dotenv import load_dotenv
import os

# Load environment variables for server IP and port
load_dotenv()
server_ip = os.getenv("SERVER_IP", "localhost")
server_port = os.getenv("SERVER_PORT", "9010")
BASE_URL = f"http://{server_ip}:{server_port}/api/v1/lights"

# Define Light IDs
light_ids = [1, 2, 5]  # List of lights to control

# Check the status of all lights
def check_light_status():
    """Retrieve and log the status of all lights."""
    url = f"{BASE_URL}/status"
    response = requests.get(url)
    if response.status_code == 200:
        light_status = response.json()
        for light_id, info in light_status.items():
            print(f"Light ID: {light_id}, Name: {info['name']}, Reachable: {info['reachable']}, On: {info['on']}")
        return light_status
    else:
        print(f"Failed to retrieve light status: {response.text}")
        return {}

# Toggle light only if it's reachable
def toggle_light(light_id, status):
    if status.get(str(light_id), {}).get("reachable", False):
        url = f"{BASE_URL}/{light_id}/toggle"
        response = requests.put(url)
        if response.status_code == 200:
            print(f"Toggled light {light_id}")
        else:
            print(f"Failed to toggle light {light_id}: {response.text}")
    else:
        print(f"Light {light_id} is not reachable. Skipping toggle.")

def set_brightness(light_id, brightness, status):
    if status.get(str(light_id), {}).get("reachable", False):
        url = f"{BASE_URL}/{light_id}/brightness/{brightness}"
        response = requests.put(url)
        if response.status_code == 200:
            print(f"Set brightness for light {light_id} to {brightness}")
        else:
            print(f"Failed to set brightness for light {light_id}: {response.text}")
    else:
        print(f"Light {light_id} is not reachable. Skipping brightness adjustment.")

def set_color(light_id, hue, sat, status):
    if status.get(str(light_id), {}).get("reachable", False):
        url = f"{BASE_URL}/{light_id}/color"
        color_data = {"hue": hue, "sat": sat}
        response = requests.put(url, json=color_data)
        if response.status_code == 200:
            print(f"Set color for light {light_id} to hue={hue}, sat={sat}")
        else:
            print(f"Failed to set color for light {light_id}: {response.text}")
    else:
        print(f"Light {light_id} is not reachable. Skipping color adjustment.")

# Dynamic light show function
def dynamic_light_show(light_id, index, status):
    """Perform a unique light show effect based on the light index, keeping brightness consistent."""
    if index % 3 == 0:
        colors = [0, 10000, 20000, 30000, 40000, 50000, 60000]
        for hue in colors:
            set_color(light_id, hue, 254, status)  # Maximum saturation
            set_brightness(light_id, 200, status)  # Maintain a high brightness level
            time.sleep(0.3)  # Shorter delay for faster transitions

    elif index % 3 == 1:
        # Smooth, constant brightness transitions without going too dim
        for _ in range(3):
            for brightness in range(150, 255, 10):  # Brightness remains above 150
                set_brightness(light_id, brightness, status)
                time.sleep(0.1)
            for brightness in range(255, 150, -10):
                set_brightness(light_id, brightness, status)
                time.sleep(0.1)

    elif index % 3 == 2:
        # Cycle through warmer color temperatures to maintain brightness
        colors = [30000, 40000, 50000, 60000, 10000, 20000, 30000]
        for hue in colors:
            set_color(light_id, hue, 254, status)
            set_brightness(light_id, 220, status)  # Slightly lower brightness for contrast
            time.sleep(0.4)  # Moderate delay for smoother effect

# Main Script
if __name__ == "__main__":
    # Check the status of lights first
    light_status = check_light_status()

    # Initialize lights by toggling them on only if they are off
    for light_id in light_ids:
        if not light_status.get(str(light_id), {}).get("on", False):
            toggle_light(light_id, light_status)
        set_brightness(light_id, 100, light_status)

    # Start a thread for each light's unique effect
    threads = []
    for index, light_id in enumerate(light_ids):
        thread = threading.Thread(target=dynamic_light_show, args=(light_id, index, light_status))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Turn off lights after the show
    for light_id in light_ids:
        toggle_light(light_id, light_status)
