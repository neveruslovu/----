import pygame
import os
import sys

# Добавляем путь для импортов
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

class HUD:
    def __init__(self, player):
        self.player = player
        self.font = pygame.font.Font(None, 36)
        print("🎯 HUD инициализирован")
    
    def draw(self, screen):
        """Отрисовка HUD"""
        try:
            # Отрисовка здоровья
            if hasattr(self.player, 'health_component'):
                health_text = f"Health: {self.player.health_component.current_health}/{self.player.health_component.max_health}"
            else:
                health_text = "Health: 100/100"
            
            health_surface = self.font.render(health_text, True, (255, 255, 255))
            screen.blit(health_surface, (10, 10))
            
            # Отрисовка уровня
            if hasattr(self.player, 'experience'):
                level_text = f"Level: {self.player.experience.current_level}"
            else:
                level_text = "Level: 1"
            
            level_surface = self.font.render(level_text, True, (255, 255, 255))
            screen.blit(level_surface, (10, 50))
            
        except Exception as e:
            print(f"❌ HUD error: {e}")
            # Минимальный HUD при ошибках
            error_text = self.font.render("HUD", True, (255, 255, 255))
            screen.blit(error_text, (10, 10))