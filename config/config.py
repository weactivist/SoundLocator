import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")

# Default values
default_config = {
    "num_leds": 72,
    "brightness": 0.1,
    "max_brightness": 0.5,
    "color_scheme": "default",
    "behavior": "full_react",
    "use_simulator": False
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
