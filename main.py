#!/usr/bin/env python3
"""
Главный файл игры - RPG Platformer
Запускает игру и управляет основным циклом
"""

import pygame
import sys
import os

# Добавляем папку game в путь импорта
sys.path.append(os.path.join(os.path.dirname(__file__), 'game'))

from game.game import Game
from game.menu import MainMenu

class Application:
    def __init__(self):
        # Инициализация pygame
        pygame.init()
        
        # Настройки окна
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("RPG Platformer")
        
        # Иконка окна
        try:
            icon = pygame.Surface((32, 32))
            icon.fill((255, 0, 0))
            pygame.display.set_icon(icon)
        except:
            pass
        
        # Часы для контроля FPS
        self.clock = pygame.time.Clock()
        self.fps = 60
        
        # Состояния приложения
        self.running = True
        self.current_state = "menu"  # menu, game, pause
        
        # Инициализация систем
        self.game = Game(self.screen)
        self.menu = MainMenu(self)
        
        print("🚀 RPG Platformer запущен!")
    
    def handle_events(self):
        """Обработка всех событий"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.current_state == "game":
                        self.current_state = "menu"
                    elif self.current_state == "menu":
                        self.running = False
                
                # Передача событий текущему состоянию
                if self.current_state == "menu":
                    self.menu.handle_event(event)
                elif self.current_state == "game":
                    self.game.handle_event(event)
    
    def update(self, dt):
        """Обновление логики игры"""
        if self.current_state == "menu":
            self.menu.update(dt)
        elif self.current_state == "game":
            self.game.update(dt)
    
    def draw(self):
        """Отрисовка игры"""
        self.screen.fill((0, 0, 0))  # Черный фон
        
        if self.current_state == "menu":
            self.menu.draw(self.screen)
        elif self.current_state == "game":
            self.game.draw(self.screen)
        
        pygame.display.flip()
    
    def run(self):
        """Главный игровой цикл"""
        try:
            while self.running:
                dt = self.clock.tick(self.fps) / 1000.0  # Delta time в секундах
                
                self.handle_events()
                self.update(dt)
                self.draw()
                
        except Exception as e:
            print(f"❌ Ошибка в игровом цикле: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            self.quit()
    
    def start_game(self):
        """Начать новую игру"""
        print("🎮 Начинаем новую игру!")
        self.current_state = "game"
        self.game = Game(self.screen)  # Пересоздаем игру
    
    def quit(self):
        """Корректный выход из игры"""
        print("👋 Выход из игры...")
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = Application()
    app.run()