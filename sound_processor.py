import numpy as np
import json
import socket
import subprocess
import time
import threading
import queue
from config.config import load_config, config
from logic.presets import PRESETS

load_config()

SOCKET_PATH = "/tmp/led.sock"
NUM_LEDS = config["num_leds"]
audio_queue = queue.Queue(maxsize=10)

RAW_SILENCE_THRESHOLD = 500


def send_led_command(command: dict):
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.connect(SOCKET_PATH)
            s.send(json.dumps(command).encode("utf-8"))
    except Exception as e:
        print(f"⚠️ LED command error: {e}")


def audio_reader():
    cmd = [
        "arecord",
        "-D", "plughw:1,0",
        "-f", "S16_LE",
        "-c", "2",
        "-r", "44100",
        "-t", "raw",
        "--buffer-size=16384",
        "--period-size=2048"
    ]

    with subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=0) as proc:
        print("🎙️ Listening with arecord in stereo mode...")
        while True:
            data = proc.stdout.read(8192)
            if not data:
                continue
            try:
                audio_queue.put_nowait(data)
            except queue.Full:
                pass  # Drop if we're behind


def audio_processor():
    preset_name = config.get("preset", "default")
    preset = PRESETS.get(preset_name, PRESETS["default"])
    behavior_func = preset["behavior"]
    color_scheme = preset["colors"]

    while True:
        try:
            data = audio_queue.get(timeout=1)
            samples = np.frombuffer(data, dtype=np.int16)
            stereo = samples.reshape(-1, 2)
            left = np.linalg.norm(stereo[:, 0])
            right = np.linalg.norm(stereo[:, 1])
            if volume_peak < max(1000, left, right):
                volume_peak = max(1000, left, right)
            print(max(left, right))
            left_brightness = 0.0 if left < RAW_SILENCE_THRESHOLD else min(1.0, (left / volume_peak))
            right_brightness = 0.0 if right < RAW_SILENCE_THRESHOLD else min(1.0, (right / volume_peak))

            leds = behavior_func(left_brightness, right_brightness, NUM_LEDS, color_scheme)

            send_led_command({
                "action": "batch",
                "pixels": [
                    {"index": i, "color": leds[i]}
                    for i in range(NUM_LEDS)
                ]
            })
            send_led_command({"action": "show"})

        except queue.Empty:
            continue
        except Exception as e:
            print(f"⚠️ Processing error: {e}")
            time.sleep(0.2)


if __name__ == "__main__":
    reader_thread = threading.Thread(target=audio_reader, daemon=True)
    processor_thread = threading.Thread(target=audio_processor, daemon=True)
    reader_thread.start()
    processor_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("👋 Exiting sound processor...")
