from .color_schemes import COLOR_SCHEMES
from .behaviors import default_behavior, directional_sweep

PRESETS = {
    "default": {
        "colors": COLOR_SCHEMES["default"],
        "behavior": default_behavior,
    },
    "directional_sweep": {
        "colors": COLOR_SCHEMES["default"],
        "behavior": directional_sweep,
    },
}