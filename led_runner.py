import json
import os
import socket
from logic.leds import HardwareStrip
from config.config import config

SOCKET_PATH = "/tmp/led.sock"

# Remove old socket if it exists
if os.path.exists(SOCKET_PATH):
    os.remove(SOCKET_PATH)

# Initialize the real LED strip
led_strip = HardwareStrip(config["num_leds"], config["brightness"])
led_strip.fill((0, 0, 0))
led_strip.show()

print("🔌 LED runner is active and listening on socket...")

with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as server:
    server.bind(SOCKET_PATH)
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
