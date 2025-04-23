# main.py
import socket
import json
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from config.config import load_config, save_config, config

SOCKET_PATH = "/tmp/led.sock"

def send_command_to_led_runner(command: dict):
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.connect(SOCKET_PATH)
            s.send(json.dumps(command).encode("utf-8"))
    except Exception as e:
        print(f"⚠️ Failed to send LED command: {e}")

# Load config from JSON
load_config()

app = FastAPI()

# Allow frontend to connect during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/brightness")
def get_brightness():
    return {"brightness": config["brightness"]}

@app.post("/brightness")
def set_brightness(value: float = Body(..., embed=True)):
    value = min(value, config["max_brightness"])
    config["brightness"] = value
    save_config()
    return {"brightness": value}

@app.post("/fill")
def fill_strip(color: tuple = Body(..., embed=True)):
    send_command_to_led_runner({"action": "fill", "color": color})
    return {"status": "filled", "color": color}

@app.post("/set_pixel")
def set_pixel(index: int = Body(...), color: tuple = Body(...)):
    send_command_to_led_runner({"action": "set_pixel", "index": index, "color": color})
    return {"status": "pixel_set", "index": index, "color": color}

@app.post("/clear")
def clear_strip():
    send_command_to_led_runner({"action": "clear"})
    return {"status": "cleared"}

@app.get("/state")
def get_state():
    return {
        "brightness": config["brightness"],
        "max_brightness": config["max_brightness"],
        "num_leds": config["num_leds"],
        "use_simulator": config.get("use_simulator", True)
    }
