"""
Система уровней - платформы, враги, предметы
"""

import pygame
from ..platform import Platform
from ..enemies.slime import Slime
from ..asset_loader import asset_loader
class Level:
    def __init__(self, name):
        print(f"🗺️ Creating level: {name}")
        self.name = name
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.background = asset_loader.load_image("backgrounds/colored_grass.png", 1)
        
        self.player = None  # Добавим ссылку на игрока
        
        self.create_test_level()
        print(f"🗺️ Уровень '{name}' создан!")
    
    def set_player(self, player):
        """Установить ссылку на игрока"""
        self.player = player
    
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
        
        # Слаймы - ставим их НА платформы
        self.enemies.add(Slime(200, 468))   # На земле (500 - 32 = 468)
        self.enemies.add(Slime(400, 318))   # На платформе (350 - 32 = 318)
        self.enemies.add(Slime(150, 368))   # На платформе (400 - 32 = 368)
    
    def update(self, dt):
        """Обновление уровня - этот метод был отсутствовал!"""
        # Обновляем врагов
        for enemy in self.enemies:
            enemy.update(dt, self)
    
    def draw(self, screen, camera):
        """Отрисовка уровня"""
        # Фон
        screen.blit(self.background, (0, 0))
        
        # Платформы
        for platform in self.platforms:
            platform.draw(screen, camera)
        
        # Враги
        for enemy in self.enemies:
            enemy.draw(screen, camera)
    
