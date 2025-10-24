# game/enemies/snail.py
import pygame
from .slime import Slime  # Наследуем от Slime для простоты

class Fly(Slime):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.speed = 1  # Улитки медленнее слаймов