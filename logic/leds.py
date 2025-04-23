from logic.strip_interface import StripInterface


try:
    import neopixel
    import board
except ImportError:
    neopixel = None
    board = None


class HardwareStrip(StripInterface):
    def __init__(self, num_leds, brightness):
        if neopixel is None or board is None:
            raise ImportError("❌ neopixel or board library not available. Make sure you're running on Raspberry Pi with proper hardware libraries installed.")

        self.num_leds = num_leds
        self.brightness = brightness
        self.strip = neopixel.NeoPixel(
            board.D18,
            num_leds,
            brightness=brightness,
            auto_write=False,
            pixel_order=neopixel.GRB
        )

    def set_pixel(self, i, color):
        if 0 <= i < self.num_leds:
            self.strip[i] = color

    def fill(self, color):
        self.strip.fill(color)

    def set_brightness(self, value):
        self.strip.brightness = value

    def show(self):
        self.strip.show()


class TerminalStrip(StripInterface):
    def __init__(self, num_leds, brightness):
        self.num_leds = num_leds
        self.leds = [(0, 0, 0)] * num_leds
        self.brightness = brightness

    def set_pixel(self, index, color):
        if 0 <= index < self.num_leds:
            self.leds[index] = color

    def fill(self, color):
        self.leds = [color] * self.num_leds

    def set_brightness(self, value):
        self.brightness = value  # simulated only, no dimming effect

    def show(self):
        output = ""
        for r, g, b in self.leds:
            output += f"\033[48;2;{r};{g};{b}m \033[0m"
        print("\r" + output, end="", flush=True)
