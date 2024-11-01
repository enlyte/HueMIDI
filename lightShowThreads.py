# lightShowThreads.py
import requests
import time
import threading
from dotenv import load_dotenv
import os

# Retrieve bridge IP and username from environment variables
load_dotenv()
bridge_ip = os.getenv("BRIDGE_IP")
username = os.getenv("USERNAME")
light_ids = [1]  # Update as needed with available Light IDs
# light_ids = [1, 2, 5]  # Light IDs to control

# Philips Hue API Functions
def set_light_state(light_id, state_data):
    """Send a command to set the light's state."""
    url = f"http://{bridge_ip}/api/{username}/lights/{light_id}/state"
    response = requests.put(url, json=state_data)
    return response.json()

def turn_on_light(light_id):
    """Turn the light on."""
    return set_light_state(light_id, {"on": True})

def turn_off_light(light_id):
    """Turn the light off."""
    return set_light_state(light_id, {"on": False})

def set_brightness(light_id, brightness):
    """Set the brightness of the light (0-254)."""
    brightness = max(0, min(brightness, 254))
    return set_light_state(light_id, {"bri": brightness})

def set_color(light_id, hue, sat=254):
    """Set the color of the light using hue (0-65535) and saturation (0-254)."""
    hue = max(0, min(hue, 65535))
    sat = max(0, min(sat, 254))
    return set_light_state(light_id, {"hue": hue, "sat": sat})

def set_temperature(light_id, ct):
    """Set the color temperature of the light (153-500)."""
    ct = max(153, min(ct, 500))
    return set_light_state(light_id, {"ct": ct})

# Light Show Threads
def light_show_1():
    """Light 1: Cycle through a set of colors."""
    if len(light_ids) > 0:
        colors = [0, 10000, 20000, 30000, 40000, 50000, 60000]
        for hue in colors:
            set_color(light_ids[0], hue)
            time.sleep(0.5)

def light_show_2():
    """Light 2: Fade brightness up and down."""
    if len(light_ids) > 1:
        for _ in range(2):  # Repeat fade twice
            for brightness in range(0, 255, 15):  # Fade up
                set_brightness(light_ids[1], brightness)
                time.sleep(0.1)
            for brightness in range(255, 0, -15):  # Fade down
                set_brightness(light_ids[1], brightness)
                time.sleep(0.1)

def light_show_3():
    """Light 3: Cycle through color temperatures."""
    if len(light_ids) > 2:
        colors = [30000, 40000, 50000, 60000, 0, 10000, 20000]
        for hue in colors:
            set_color(light_ids[2], hue)
            time.sleep(0.5)

# Main Script
if __name__ == "__main__":
    # Turn on all lights initially
    for light_id in light_ids:
        turn_on_light(light_id)
        set_brightness(light_id, 100)

    # Start threads for each light's unique effect
    thread1 = threading.Thread(target=light_show_1)
    thread2 = threading.Thread(target=light_show_2)
    thread3 = threading.Thread(target=light_show_3)

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
        turn_off_light(light_id)

