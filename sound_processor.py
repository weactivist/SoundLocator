import sounddevice as sd
import numpy as np
import json
import socket
import time
from config.config import load_config, config

load_config()

SOCKET_PATH = "/tmp/led.sock"


def send_led_command(command: dict):
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.connect(SOCKET_PATH)
            s.send(json.dumps(command).encode("utf-8"))
    except Exception as e:
        print(f"⚠️ LED command error: {e}")


def stereo_callback(indata, frames, time_info, status):
    if status:
        print(f"⚠️ Sound input warning: {status}")
    if indata.shape[1] < 2:
        return

    left = np.linalg.norm(indata[:, 0])
    right = np.linalg.norm(indata[:, 1])

    left_brightness = min(1.0, left * 20)
    right_brightness = min(1.0, right * 20)

    num_half = config["num_leds"] // 2

    leds = [(0, 0, 0)] * config["num_leds"]

    left_value = int(255 * left_brightness)
    right_value = int(255 * right_brightness)

    for i in range(num_half):
        leds[i] = (left_value, 0, 0)
    for i in range(num_half, config["num_leds"]):
        leds[i] = (0, 0, right_value)

    send_led_command({"action": "fill", "color": [0, 0, 0]})  # Clear first
    for i, color in enumerate(leds):
        send_led_command({"action": "set_pixel", "index": i, "color": color})
    send_led_command({"action": "show"})


if __name__ == "__main__":
    print("🎙️ Starting sound processor...")
    with sd.InputStream(channels=2, callback=stereo_callback, samplerate=44100, blocksize=1024):
        while True:
            time.sleep(0.1)
