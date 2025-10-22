"""
Система камеры для следования за игроком
"""

import pygame

class Camera:
    def __init__(self, target, screen_size):
        self.target = target
        self.screen_size = screen_size
        self.offset = pygame.math.Vector2(0, 0)
        self.offset_float = pygame.math.Vector2(0, 0)
        
        # Константы для плавного слежения
        self.CONST = pygame.math.Vector2(
            -screen_size[0] / 2 + target.rect.width / 2,
            -screen_size[1] / 2 + target.rect.height / 2
        )
        
        print("📷 Камера инициализирована!")
    
    def update(self):
        """Обновление позиции камеры"""
        if self.target:
            # Плавное слежение за целью
            self.offset_float.x += (self.target.rect.x - self.offset_float.x + self.CONST.x) * 0.05
            self.offset_float.y += (self.target.rect.y - self.offset_float.y + self.CONST.y) * 0.05
            
            # Округление для избежания артефактов
            self.offset.x, self.offset.y = int(self.offset_float.x), int(self.offset_float.y)
    
    def apply(self, rect):
        """Применение смещения камеры к прямоугольнику"""
        return rect.move(-self.offset.x, -self.offset.y)
    
    def apply_point(self, point):
        """Применение смещения камеры к точке"""
        return (point[0] - self.offset.x, point[1] - self.offset.y)