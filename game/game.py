"""
Основной класс игры, управляющий всеми системами
"""

import pygame
from .player import Player
from .camera import Camera
from .level import Level
from .combat import CombatSystem
from ..ui.hud import HUD

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.screen_size = screen.get_size()
        
        # Инициализация систем
        self.level = Level("forest_01")
        self.player = Player(100, 300)
        self.camera = Camera(self.player, self.screen_size)
        self.combat_system = CombatSystem(self)
        self.hud = HUD(self.player)
        
        # Устанавливаем игрока в уровне
        self.level.set_player(self.player)
        
        # Состояние игры
        self.running = True
        self.paused = False
        
        print("🎮 Игра инициализирована!")
    
    def handle_events(self, events):
        """Обработка событий игры"""
        for event in events:
            self.handle_event(event)
    
    def handle_event(self, event):
        """Обработка событий игры"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                self.paused = not self.paused
                print(f"{'⏸️ Пауза' if self.paused else '▶️ Продолжить'}")
    
    def update(self, dt):
        """Обновление состояния игры"""
        # Обработка непрерывного ввода (клавиши)
        keys = pygame.key.get_pressed()
        self.player.handle_keys(keys)
    
        # Обновление игрока - передаем platforms из уровня
        if hasattr(self.level, 'platforms'):
            self.player.update(self.level.platforms)
        elif hasattr(self.level, 'tiles'):
            self.player.update(self.level.tiles)
        else:
            # Если нет platforms, передаем пустой список
            self.player.update([])
    
        # Обновление камеры (без передачи player, если не нужно)
        try:
            self.camera.update(self.player)  # Пробуем с аргументом
        except TypeError:
            try:
                self.camera.update()  # Пробуем без аргумента
            except Exception as e:
                print(f"Camera update error: {e}")
    
        # Обновление уровня (враги и т.д.)
        if hasattr(self.level, 'update'):
            self.level.update(dt)
    
    def draw(self, screen):
        """Отрисовка игры"""
        # Отрисовка уровня
        self.level.draw(screen, self.camera)
        
        # Отрисовка игрока
        self.player.draw(screen, self.camera)
        
        # Отрисовка HUD поверх всего
        self.hud.draw(screen)
        
        # Отрисовка паузы
        if self.paused:
            self.draw_pause_screen(screen)
    
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