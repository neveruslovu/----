import pygame
import os
import sys

# Добавляем путь к корню проекта для абсолютных импортов
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from game.player import Player
from game.camera import Camera
from game.level import Level
from ui.hud import HUD  # Теперь это абсолютный импорт

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.camera = Camera(Player(100, 300), (800, 600))  # Создаем временного игрока для камеры
        self.level = Level("forest_01")
        
        # Создаем игрока после уровня
        self.player = Player(100, 300)
        self.camera.target = self.player  # Обновляем цель камеры
        
        # Создаем HUD
        self.hud = HUD(self.player)
        
        print("🎮 Игра инициализирована!")
    
    def handle_events(self, events):
        """Обработка событий игры"""
        for event in events:
            self.handle_event(event)
    
    def handle_event(self, event):
        """Обработка одиночного события"""
        self.player.handle_event(event)
    
    def update(self, dt):
        """Обновление состояния игры"""
        # Обработка непрерывного ввода (клавиши)
        keys = pygame.key.get_pressed()
        self.player.handle_keys(keys)
        
        # Обновление игрока
        self.player.update(self.level.platforms)
        
        # Обновление камеры
        self.camera.update()
        
        # Обновление уровня
        self.level.update(dt)
    
    def draw(self, screen):
        """Отрисовка игры"""
        # Очистка экрана
        screen.fill((135, 206, 235))  # Голубой фон
        
        # Отрисовка уровня
        self.level.draw(screen, self.camera)
        
        # Отрисовка игрока
        self.player.draw(screen, self.camera)
        
        # Отрисовка HUD
        self.hud.draw(screen)
    
    def draw_pause_screen(self, screen):
        """Отрисовка экрана паузы"""
        # Полупрозрачный overlay
        overlay = pygame.Surface(self.screen_size, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))
        
        # Текст паузы
        font = pygame.font.Font(None, 72)
        text = font.render("ПАУЗА", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.screen_size[0]//2, self.screen_size[1]//2))
        screen.blit(text, text_rect)
        
        # Инструкция
        small_font = pygame.font.Font(None, 36)
        instruction = small_font.render("Нажмите P для продолжения", True, (200, 200, 200))
        instruction_rect = instruction.get_rect(center=(self.screen_size[0]//2, self.screen_size[1]//2 + 60))
        screen.blit(instruction, instruction_rect)