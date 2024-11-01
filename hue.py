import requests
import mido
import time
from dotenv import load_dotenv
import os

# Retrieve bridge IP and username from environment variables
load_dotenv()
bridge_ip = os.getenv("BRIDGE_IP")
username = os.getenv("USERNAME")
light_id = 5  # Set the light ID you want to control

# Light ID: 1, Name: Color One
# Light ID: 2, Name: Color Two
# Light ID: 3, Name: Hue white lamp 1
# Light ID: 4, Name: Hue white lamp 2
# Light ID: 5, Name: Color Three

# Philips Hue API Functions
def set_light_state(state_data):
    """Send a command to set the light's state."""
    url = f"http://{bridge_ip}/api/{username}/lights/{light_id}/state"
    response = requests.put(url, json=state_data)
    return response.json()

def turn_on_light():
    """Turn the light on."""
    return set_light_state({"on": True})

def turn_off_light():
    """Turn the light off."""
    return set_light_state({"on": False})

def set_brightness(brightness):
    """Set the brightness of the light (0-254)."""
    brightness = max(0, min(brightness, 254))  # Clamp brightness between 0-254
    return set_light_state({"bri": brightness})

def set_color(hue, sat=254):
    """Set the color of the light using hue (0-65535) and saturation (0-254)."""
    hue = max(0, min(hue, 65535))  # Clamp hue between 0-65535
    sat = max(0, min(sat, 254))    # Clamp saturation between 0-254
    return set_light_state({"hue": hue, "sat": sat})

def set_temperature(ct):
    """Set the color temperature of the light (153-500)."""
    ct = max(153, min(ct, 500))  # Clamp ct between 153-500
    return set_light_state({"ct": ct})

def cycle_colors():
    """Cycle through a set of colors."""
    colors = [0, 10000, 20000, 30000, 40000, 50000, 60000]
    for hue in colors:
        set_color(hue)
        time.sleep(1)

# MIDI Event Handling
def process_midi_message(message):
    """Process incoming MIDI messages and map them to light functions."""
    if message.type == 'note_on':
        if message.note == 60:  # Middle C
            turn_on_light()
        elif message.note == 62:  # D key
            turn_off_light()
        elif message.note == 64:  # E key
            set_brightness(200)
        elif message.note == 65:  # F key
            set_brightness(50)
        elif message.note == 67:  # G key
            cycle_colors()

    elif message.type == 'control_change':
        if message.control == 1:  # Modulation wheel (brightness control)
            brightness_value = int((message.value / 127) * 254)
            set_brightness(brightness_value)

        elif message.control == 2:  # Another MIDI control (hue control)
            hue_value = int((message.value / 127) * 65535)
            set_color(hue_value)

        elif message.control == 3:  # Another MIDI control (temperature control)
            ct_value = int((message.value / 127) * 347 + 153)
            set_temperature(ct_value)

# Main MIDI Loop
def listen_for_midi():
    """Listen for MIDI inputs and map to light functions."""
    with mido.open_input('Your MIDI Device Name') as inport:
        print("Listening for MIDI inputs...")
        for msg in inport:
            process_midi_message(msg)

# Main Script
if __name__ == "__main__":
    # Turn on light initially
    turn_on_light()
    set_brightness(100)
    set_color(10000)  # A soft white color

    # Start listening for MIDI inputs
    # listen_for_midi()
