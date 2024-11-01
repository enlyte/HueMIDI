# lightShow1.py
import requests
import time
from dotenv import load_dotenv
import os

# Retrieve bridge IP and username from environment variables
load_dotenv()
bridge_ip = os.getenv("BRIDGE_IP")
username = os.getenv("USERNAME")
light_ids = [1, 2, 5]  # List of lights to control

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

# Light Show Functions
def cycle_colors(lights, duration=10):
    """Cycle through colors on multiple lights for a given duration."""
    colors = [0, 10000, 20000, 30000, 40000, 50000, 60000]
    start_time = time.time()
    while time.time() - start_time < duration:
        for hue in colors:
            for light_id in lights:
                set_color(light_id, hue)
            time.sleep(0.5)  # Change every 0.5 seconds

def fade_brightness(lights, duration=5):
    """Fade brightness up and down on multiple lights for a given duration."""
    start_time = time.time()
    while time.time() - start_time < duration:
        for brightness in range(0, 255, 15):  # Fade up
            for light_id in lights:
                set_brightness(light_id, brightness)
            time.sleep(0.1)
        for brightness in range(255, 0, -15):  # Fade down
            for light_id in lights:
                set_brightness(light_id, brightness)
            time.sleep(0.1)

def change_temperature(lights, duration=5):
    """Cycle through color temperatures on multiple lights for a given duration."""
    temperatures = [153, 200, 300, 400, 500]
    start_time = time.time()
    while time.time() - start_time < duration:
        for ct in temperatures:
            for light_id in lights:
                set_temperature(light_id, ct)
            time.sleep(0.5)

# Main Script
if __name__ == "__main__":
    # Turn on all lights initially
    for light_id in light_ids:
        turn_on_light(light_id)
        set_brightness(light_id, 100)
        set_color(light_id, 10000)  # Set an initial soft white color

    # Run a small light show
    cycle_colors(light_ids, duration=5)
    fade_brightness(light_ids, duration=3)
    change_temperature(light_ids, duration=2)

    # Turn off lights after the show
    for light_id in light_ids:
        turn_off_light(light_id)

    # Start listening for MIDI inputs (uncomment when using a MIDI controller)
    # listen_for_midi()
