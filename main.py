# main.py
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from config.config import load_config, save_config, config

# Load config from JSON
load_config()

# Import appropriate strip class based on config
if config.get("use_simulator", True):
    from logic.leds import TerminalStrip as Strip
else:
    from logic.leds import HardwareStrip as Strip

app = FastAPI()

# Allow frontend to connect during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize strip
led_strip = Strip(config["num_leds"], config["brightness"])
led_strip.fill((0, 0, 0))
led_strip.show()

@app.get("/brightness")
def get_brightness():
    return {"brightness": config["brightness"]}

@app.post("/brightness")
def set_brightness(value: float = Body(..., embed=True)):
    value = min(value, config["max_brightness"])
    config["brightness"] = value
    led_strip.set_brightness(value)
    save_config()
    return {"brightness": value}

@app.post("/fill")
def fill_strip(color: tuple = Body(..., embed=True)):
    led_strip.fill(color)
    led_strip.show()
    return {"status": "filled", "color": color}

@app.post("/set_pixel")
def set_pixel(index: int = Body(...), color: tuple = Body(...)):
    led_strip.set_pixel(index, color)
    led_strip.show()
    return {"status": "pixel_set", "index": index, "color": color}

@app.post("/clear")
def clear_strip():
    led_strip.fill((0, 0, 0))
    led_strip.show()
    return {"status": "cleared"}

@app.get("/state")
def get_state():
    return {
        "brightness": config["brightness"],
        "max_brightness": config["max_brightness"],
        "num_leds": config["num_leds"],
        "use_simulator": config.get("use_simulator", True)
    }