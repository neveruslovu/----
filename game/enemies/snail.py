# game/enemies/snail.py
import pygame
from game.enemies.slime import Slime

class Snail(Slime):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.speed = 1  # Улитки медленнее слаймов