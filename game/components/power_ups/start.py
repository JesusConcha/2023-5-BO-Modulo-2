from game.components.power_ups.power_up import PowerUps
from game.utils.constants import HEART, HEART_TYPE


class Start(PowerUps):
    def __init__(self):
        super().__init__(HEART, HEART_TYPE)
