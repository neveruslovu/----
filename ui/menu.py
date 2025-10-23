import pygame
import sys
import os

# Добавляем пути для импортов
sys.path.append(os.path.dirname(__file__))

from ui.menu import MainMenu
from game.game import Game

class Application:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("RPG Platformer")
        
        self.current_state = "menu"
        self.main_menu = MainMenu(self)
        self.game = None
        self.running = True
        
        print("🎮 Application initialized")

    def start_game(self):
        """Запуск новой игры"""
        print("🚀 START_GAME called - switching to game state")
        self.current_state = "game"
        self.game = Game(self.screen)
        print(f"✅ Game started, state: {self.current_state}")

    def run(self):
        """Главный игровой цикл"""
        clock = pygame.time.Clock()
        
        print("🎮 Starting main loop...")
        print("💡 Use UP/DOWN arrows or mouse to navigate menu")
        print("💡 Press ENTER or click to select")
        
        while self.running:
            dt = clock.tick(60) / 1000.0
            
            # Обработка событий
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.current_state == "game":
                            self.current_state = "menu"
                            print("↩️ Returning to menu")
            
            # Обработка состояний
            if self.current_state == "menu":
                for event in events:
                    self.main_menu.handle_event(event)
                self.main_menu.update(dt)
                self.main_menu.draw(self.screen)
                
            elif self.current_state == "game":
                # Игровой режим
                self.game.handle_events(events)
                self.game.update(dt)
                self.game.draw(self.screen)
            
            pygame.display.flip()
        
        print("👋 Game ended")
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = Application()
    app.run()