import json
import os
import socket
import time
import signal
import sys
from config.config import load_config, config

load_config()

if config.get("use_simulator", True):
    from logic.leds import TerminalStrip as Strip
else:
    from logic.leds import HardwareStrip as Strip

SOCKET_PATH = "/tmp/led.sock"

# Remove old socket if it exists
if os.path.exists(SOCKET_PATH):
    os.remove(SOCKET_PATH)

# Initialize the LED strip
led_strip = Strip(config["num_leds"], config["brightness"])
led_strip.fill((0, 0, 0))
led_strip.show()

print(f"🔌 LED runner ({'Simulator' if config.get('use_simulator') else 'Hardware'}) is active and listening on socket...")

def onoff_sequence(strip, color):
    length = strip.num_leds
    center = length // 2
    for i in range(center):
        strip.set_pixel(center + i, (color, color, color))
        strip.set_pixel(center - i - 1, (color, color, color))
        strip.show()
        time.sleep(0.02)
    # Fade out
    for b in range(color, -1, -15):
        dim_color = (b, b, b)
        strip.fill(dim_color)
        strip.show()
        time.sleep(0.02)

def lightspeed_startup(strip):
    onoff_sequence(strip, 255)
    print("🚀 Lightspeed jump sequence complete")

def shutdown_sequence(strip):
    onoff_sequence(strip, 150)
    print("💤 Vader's fade shutdown complete")

def graceful_exit(signum, frame):
    print("🚦 Shutting down gracefully...")
    shutdown_sequence(led_strip)
    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)
    sys.exit(0)

signal.signal(signal.SIGINT, graceful_exit)
signal.signal(signal.SIGTERM, graceful_exit)

# Run lightspeed jump on startup
lightspeed_startup(led_strip)

with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as server:
    server.bind(SOCKET_PATH)
    os.chmod(SOCKET_PATH, 0o666)
    server.listen()

    while True:
        conn, _ = server.accept()
        with conn:
            try:
                data = conn.recv(1024)
                if not data:
                    continue

                command = json.loads(data.decode("utf-8"))
                action = command.get("action")

                if action == "fill":
                    color = tuple(command.get("color", [0, 0, 0]))
                    led_strip.fill(color)
                    led_strip.show()
                    print(f"✅ Filled with color {color}")

                elif action == "set_pixel":
                    i = command.get("index")
                    color = tuple(command.get("color", [0, 0, 0]))
                    if i is not None:
                        led_strip.set_pixel(i, color)
                        led_strip.show()
                        print(f"✅ Set pixel {i} to {color}")

                elif action == "clear":
                    led_strip.fill((0, 0, 0))
                    led_strip.show()
                    print("✅ Strip cleared")

            except Exception as e:
                print(f"⚠️ Error processing command: {e}")