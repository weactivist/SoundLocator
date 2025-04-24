import numpy as np
import json
import socket
import subprocess
import time
from config.config import load_config, config

load_config()

SOCKET_PATH = "/tmp/led.sock"
NUM_LEDS = config["num_leds"]


def send_led_command(command: dict):
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.connect(SOCKET_PATH)
            s.send(json.dumps(command).encode("utf-8"))
    except Exception as e:
        print(f"⚠️ LED command error: {e}")


def process_audio_stream():
    cmd = [
        "arecord", 
        "-D", "plughw:1,0",
        "-f", "S16_LE", 
        "-c", "2", 
        "-r", "44100", 
        "-t", "raw",
        "--buffer-size=8192",
        "--period-size=2048"
    ]

    with subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=2048) as proc:
        print("🎙️ Listening with arecord in stereo mode...")
        while True:
            try:
                data = proc.stdout.read(8192)  # 1024 frames, 2 channels, 16-bit
                if not data:
                    continue
                samples = np.frombuffer(data, dtype=np.int16)
                stereo = samples.reshape(-1, 2)
                left = np.linalg.norm(stereo[:, 0])
                right = np.linalg.norm(stereo[:, 1])

                left_brightness = min(1.0, left / 10000)
                right_brightness = min(1.0, right / 10000)

                l_val = int(255 * left_brightness)
                r_val = int(255 * right_brightness)

                num_half = NUM_LEDS // 2
                leds = [(0, 0, 0)] * NUM_LEDS

                for i in range(num_half):
                    leds[i] = (l_val, 0, 0)
                for i in range(num_half, NUM_LEDS):
                    leds[i] = (0, 0, r_val)

                send_led_command({
                    "action": "batch",
                    "pixels": [
                        {"index": i, "color": color}
                        for i, color in enumerate(leds)
                    ]
                })
                send_led_command({"action": "show"})

                time.sleep(0.15)
            except Exception as e:
                print(f"⚠️ Processing error: {e}")
                time.sleep(0.2)


if __name__ == "__main__":
    process_audio_stream()
