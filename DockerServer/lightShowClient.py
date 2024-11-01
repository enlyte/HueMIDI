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

light_ids = [1, 2, 5]  # Light IDs to control

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

# Light Show Threads
def light_show_1(status):
    """Light 1: Cycle through a set of colors."""
    colors = [0, 10000, 20000, 30000, 40000, 50000, 60000]
    for hue in colors:
        set_color(light_ids[0], hue, 254, status)
        time.sleep(0.5)

def light_show_2(status):
    """Light 2: Fade brightness up and down."""
    for _ in range(2):
        for brightness in range(0, 255, 15):
            set_brightness(light_ids[1], brightness, status)
            time.sleep(0.1)
        for brightness in range(255, 0, -15):
            set_brightness(light_ids[1], brightness, status)
            time.sleep(0.1)

def light_show_3(status):
    """Light 3: Cycle through color temperatures."""
    colors = [30000, 40000, 50000, 60000, 0, 10000, 20000]
    for hue in colors:
        set_color(light_ids[2], hue, 254, status)
        time.sleep(0.5)

# Main Script
if __name__ == "__main__":
    # Check the status of lights first
    light_status = check_light_status()

    # Initialize lights by toggling them on if reachable
    for light_id in light_ids:
        toggle_light(light_id, light_status)
        set_brightness(light_id, 100, light_status)

    # Start threads for each light's unique effect
    thread1 = threading.Thread(target=light_show_1, args=(light_status,))
    thread2 = threading.Thread(target=light_show_2, args=(light_status,))
    thread3 = threading.Thread(target=light_show_3, args=(light_status,))

    # Start the threads
    thread1.start()
    thread2.start()
    thread3.start()

    # Wait for all threads to complete
    thread1.join()
    thread2.join()
    thread3.join()

    # Turn off lights after the show
    for light_id in light_ids:
        toggle_light(light_id, light_status)
