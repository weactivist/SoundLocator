from abc import ABC, abstractmethod
from typing import Tuple


class StripInterface(ABC):
    @abstractmethod
    def __init__(self, num_leds: int, brightness: float):
        pass

    @abstractmethod
    def fill(self, color: Tuple[int, int, int]):
        pass

    @abstractmethod
    def set_pixel(self, i: int, color: Tuple[int, int, int]):
        pass

    @abstractmethod
    def set_brightness(self, value: float):
        pass

    @abstractmethod
    def show(self):
        pass
