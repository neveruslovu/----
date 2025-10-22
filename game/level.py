"""
Система уровней - платформы, враги, предметы
"""

import pygame
from .platform import Platform
from .enemies.slime import Slime

class Level:
    def __init__(self, name):
        self.name = name
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.background_color = (135, 206, 235)  # Небесно-голубой
        
        self.create_test_level()
        print(f"🗺️ Уровень '{name}' создан!")
    
    def create_test_level(self):
        """Создание тестового уровня"""
        # Земля
        for x in range(-100, 900, 32):
            self.platforms.add(Platform(x, 500, 32, 32))
        
        # Платформы
        platforms_data = [
            (100, 400, 100, 20),
            (300, 350, 100, 20),
            (500, 300, 100, 20),
            (200, 250, 100, 20),
            (400, 200, 100, 20),
        ]
        
        for x, y, w, h in platforms_data:
            self.platforms.add(Platform(x, y, w, h))
        
        # Враги
        self.enemies.add(Slime(200, 450))
        self.enemies.add(Slime(400, 300))
    
    def update(self, dt):
        """Обновление уровня"""
        self.enemies.update(dt, self)
    
    def draw(self, screen, camera):
        """Отрисовка уровня"""
        # Фон
        screen.fill(self.background_color)
        
        # Платформы
        for platform in self.platforms:
            platform.draw(screen, camera)
        
        # Враги
        for enemy in self.enemies:
            enemy.draw(screen, camera)