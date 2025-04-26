import numpy as np
import json
import socket
import subprocess
import time
import threading
import queue
from config.config import load_config, config

load_config()

SOCKET_PATH = "/tmp/led.sock"
NUM_LEDS = config["num_leds"]
audio_queue = queue.Queue(maxsize=10)


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
    while True:
        try:
            data = audio_queue.get(timeout=1)
            samples = np.frombuffer(data, dtype=np.int16)
            stereo = samples.reshape(-1, 2)
            left = np.linalg.norm(stereo[:, 0])
            right = np.linalg.norm(stereo[:, 1])

            left_brightness = min(1.0, left / 10000)
            right_brightness = min(1.0, right / 10000)

            leds = [(0, 0, 0)] * NUM_LEDS
            center = NUM_LEDS // 2

            # Define quarters
            left_quarter = center // 4
            right_quarter = center // 4

            for i in range(center):
                if i < left_quarter:
                    color = (139, 0, 0)  # Dark Red
                elif i < 2 * left_quarter:
                    color = (255, 69, 0)  # Red-Orange (new color)
                elif i < 3 * left_quarter:
                    color = (255, 165, 0)  # Orange
                else:
                    color = (128, 0, 128)  # Purple
                if i / center < left_brightness:
                    leds[i] = color

            for i in range(center, NUM_LEDS):
                if (NUM_LEDS - i - 1) < right_quarter:
                    color = (0, 0, 139)  # Deep Blue
                elif (NUM_LEDS - i - 1) < 2 * right_quarter:
                    color = (0, 0, 255)  # Blue
                elif (NUM_LEDS - i - 1) < 3 * right_quarter:
                    color = (0, 255, 255)  # Cyan
                else:
                    color = (128, 0, 128)  # Purple
                if (NUM_LEDS - i) / center < right_brightness:
                    leds[i] = color

            send_led_command({
                "action": "batch",
                "pixels": [
                    {"index": i, "color": color}
                    for i, color in enumerate(leds)
                ]
            })
            send_led_command({"action": "show"})
            time.sleep(0.1)

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
