import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")

# Default values
default_config = {
    "num_leds": 72,  # Number of LEDs on the strip.
    "brightness": 0.1,  # Set initial brightness. Default is 10%.
    "max_brightness": 0.1,  # Max brightness. Default is 10%. Warning: Calculate how much power you have to run the strips.
    "preset": "default",  # Set color scheme.
    "use_simulator": False  # Use terminal simulation of LED lights. Hardware strip by default.
}

# In-memory config dictionary
config = {}

def load_config():
    global config
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            config.update(json.load(f))
    else:
        config.update(default_config)
        save_config()

def save_config():
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)
