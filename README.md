## Deploy
Create a new file `/config/config.json` and change whatever settings you'd like. Full set of settings can be found in `/config/config.py`.

Start the app: `poetry run uvicorn main:app`

## Development
Add `"use_simulator": true` to `/config/config.json` to simulate the LEDs within a terminal.

Start the app: `poetry run uvicorn main:app --reload`