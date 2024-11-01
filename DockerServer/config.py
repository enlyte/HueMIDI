import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

class Config:
    bridge_ip = os.getenv("BRIDGE_IP")
    username = os.getenv("USERNAME")
    lights = {
        "light_1": int(os.getenv("LIGHT_1_ID", 1)),
        "light_2": int(os.getenv("LIGHT_2_ID", 2)),
        "light_3": int(os.getenv("LIGHT_3_ID", 3)),
    }
