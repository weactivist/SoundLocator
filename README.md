**Project is work in progress! Do not use yet.**

# 🎧 SoundLocator
SoundLocator is a stereo sound-reactive LED controller powered by FastAPI and running on a Raspberry Pi. It captures audio from a connected PC and visualizes it in real time using a WS2812B LED strip making it ideal for hearing impaired gamers or if you'd like some cool vizual audio effects. The system includes a web-based UI and API for controlling brightness, color schemes, and behavior presets

## 📦 Prerequisites
- Raspberry Pi with Raspberry Pi OS installed.
- Addressable RGB LED strip like WS2812B 5V DC.
- LED strip wired to Raspberry Pi.
- USB sound card with 3.5mm analog audio input.
- 3.5mm male-to-male stereo audio cable

## 🔌 LED strip wiring
Your LED strip has at least three wires (sometimes five, if duplicated):

- GND (usually white or black)
- 5V (usually red)
- DIN (data input, usually green)

| LED Strip Wire | Connects To (Raspberry Pi Pin) | Notes |
|---|---|---|
| GND | Pin 6 (or any GND) | Must be a shared ground with Pi |
| 5V | Pin 2 or 4 (5V) | OK for low-brightness use (≤ ~10%) |
| DIN | Pin 12 (GPIO18) | Use a 330Ω resistor in line to reduce signal noise |

## 🧑‍💻 Setup
1. SSH to your Raspberry Pi.
2. Install Git (if not already)
```bash
sudo apt update
sudo apt install git
```
3. Clone GitHub repo
```bash
git clone https://github.com/weactivist/soundlocator.git
cd soundlocator
```
4. Install Poetry
```bash
curl -sSL https://install.python-poetry.org | python3 -
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```
5. Install dependencies
```bash
poetry install
```
6. Edit config (available settings can be found in `config/config.py`)
```bash
nano config/config.json
```
Example:
```json
{
    "num_leds": 72,
    "brightness": 0.1,
    "max_brightness": 0.1,
    "color_scheme": "default"
}
```
7. Run the app
```bash
poetry run uvicorn main:app --host 0.0.0.0 --port 8000
```

UI available at: http://<ip_address>/docs/:8000

## 🧑‍💻 To pull future updates
```
git pull
poetry install
```

## ⚙️ Development
Add `"use_simulator": true` to `config/config.json` to simulate the LEDs in a terminal window.

Start the app: `poetry run uvicorn main:app --reload`