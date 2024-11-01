from fastapi import FastAPI, WebSocket, HTTPException
from pydantic import BaseModel
import requests
import os
import logging
from config import Config

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()

# Philips Hue API URL setup
HUE_API_URL = f"http://{Config.bridge_ip}/api/{Config.username}/lights"

class LightState(BaseModel):
    brightness: int = None
    hue: int = None
    sat: int = 254

def fetch_lights_data():
    """Fetch and process light data from the Philips Hue API."""
    try:
        response = requests.get(HUE_API_URL)
        response.raise_for_status()
        lights = response.json()

        # Process response structure (dict or list) into a unified format
        processed_lights = {}
        if isinstance(lights, dict):
            for light_id, info in lights.items():
                processed_lights[light_id] = {
                    "name": info["name"],
                    "reachable": info["state"].get("reachable", False),
                    "on": info["state"].get("on", False),
                    "state": info["state"]
                }
        elif isinstance(lights, list):
            for index, info in enumerate(lights):
                processed_lights[str(index)] = {
                    "name": info.get("name", "Unknown"),
                    "reachable": info.get("state", {}).get("reachable", False),
                    "on": info.get("state", {}).get("on", False),
                    "state": info.get("state", {})
                }
        else:
            logger.error("Unexpected lights response format.")
            raise HTTPException(status_code=500, detail="Unexpected lights response format")

        logger.info("Successfully processed lights data.")
        return processed_lights
    except requests.exceptions.RequestException as e:
        logger.error("Failed to retrieve lights data: %s", str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve lights data")

# Endpoint to check the status of all lights
@app.get("/api/v1/lights/status")
def check_light_status():
    status_info = fetch_lights_data()
    return {light_id: {k: v for k, v in info.items() if k != "state"} for light_id, info in status_info.items()}

# Endpoint to retrieve all lights
@app.get("/api/v1/lights")
def get_lights():
    return fetch_lights_data()

# Toggle light with enhanced reachability checks and error handling
@app.put("/api/v1/lights/{light_id}/toggle")
def toggle_light(light_id: int):
    lights = fetch_lights_data()
    if str(light_id) not in lights:
        logger.error(f"Light {light_id} not found in response.")
        raise HTTPException(status_code=404, detail="Light not found")

    light_info = lights[str(light_id)]
    if not light_info["reachable"]:
        logger.error(f"Light {light_id} is not reachable.")
        raise HTTPException(status_code=503, detail="Light not reachable")

    # Toggle based on current state
    current_state = light_info["on"]
    toggle_data = {"on": not current_state}

    # Send the toggle request
    state_url = f"{HUE_API_URL}/{light_id}/state"
    try:
        toggle_response = requests.put(state_url, json=toggle_data)
        toggle_response.raise_for_status()
        logger.info(f"Toggled light {light_id} to {'on' if not current_state else 'off'}")
        return toggle_response.json()
    except requests.exceptions.RequestException as e:
        logger.error("Failed to toggle light %d: %s", light_id, str(e))
        raise HTTPException(status_code=500, detail="Failed to toggle light")

# Set brightness
@app.put("/api/v1/lights/{light_id}/brightness/{value}")
def set_brightness(light_id: int, value: int):
    state_url = f"{HUE_API_URL}/{light_id}/state"
    brightness_data = {"bri": min(max(value, 0), 254)}

    try:
        response = requests.put(state_url, json=brightness_data)
        response.raise_for_status()
        logger.info("Set brightness for light %d to %d", light_id, value)
        return response.json()
    
    except requests.exceptions.RequestException as e:
        logger.error("Failed to set brightness for light %d: %s", light_id, str(e))
        raise HTTPException(status_code=500, detail="Failed to set brightness")

# Set color
@app.put("/api/v1/lights/{light_id}/color")
def set_color(light_id: int, light_state: LightState):
    state_url = f"{HUE_API_URL}/{light_id}/state"
    color_data = {"hue": light_state.hue, "sat": light_state.sat}

    try:
        response = requests.put(state_url, json=color_data)
        response.raise_for_status()
        logger.info("Set color for light %d: hue=%d, sat=%d", light_id, light_state.hue, light_state.sat)
        return response.json()
    
    except requests.exceptions.RequestException as e:
        logger.error("Failed to set color for light %d: %s", light_id, str(e))
        raise HTTPException(status_code=500, detail="Failed to set color")

# WebSocket for MIDI control
@app.websocket("/api/v1/midi")
async def midi_websocket(websocket: WebSocket):
    await websocket.accept()
    logger.info("MIDI WebSocket connection accepted")
    while True:
        try:
            data = await websocket.receive_text()
            logger.info("Received MIDI data: %s", data)
            # Process MIDI data here to control lights
            await websocket.send_text(f"Received data: {data}")
        except Exception as e:
            logger.error("WebSocket connection error: %s", str(e))
            break
