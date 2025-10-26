import pygame
import sys
import os

# Добавляем путь для импортов
sys.path.append(os.path.dirname(__file__))

from game.player import Player
from game.camera import Camera
from game.levels.level1 import Level
from ui.menu import MainMenu
from ui.hud import HUD

class RPGPlatformer:
    def __init__(self):
        pygame.init()
        
        # Настройки экрана
        self.SCREEN_WIDTH = 1400
        self.SCREEN_HEIGHT = 800
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("RPG PLATFORMER")
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "menu"  # menu, game, settings
        
        # Инициализация систем
        self.menu = MainMenu(self)
        self.player = None
        self.level = None
        self.camera = None
        self.hud = None
        
        # ⏰ ДОБАВЛЕНО: Переменная для отслеживания времени игры
        self.game_start_time = 0
        
        print("🎮 RPG Platformer инициализирован!")
    
    def start_game(self):
        """Запуск новой игры"""
        print("🚀 Запуск новой игры...")
        self.state = "game"
        self.game_start_time = pygame.time.get_ticks()
    
        try:
            # 🔥 ВАЖНО: Сначала создаем уровень, потом игрока
            self.level = Level("level1")
            
        
            # 🔥 ИГРОК СОЗДАЕТСЯ В ПОЗИЦИИ (0,0), НО СРАЗУ ПЕРЕМЕЩАЕТСЯ
            self.player = Player(0, 0)
       
        
            # 🔥 УСТАНАВЛИВАЕМ ИГРОКА В УРОВНЕ (ЭТО ПЕРЕМЕСТИТ ЕГО НА СПАВН)
            self.level.set_player(self.player)   
                     
            self.camera = Camera(self.player, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
            self.hud = HUD(self.player)
        
            print("✅ Игра запущена!")
        
        except Exception as e:
            print(f"❌ Ошибка при запуске игры: {e}")
            import traceback
            traceback.print_exc()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # Передаем события в текущее состояние
            if self.state == "menu":
                self.menu.handle_event(event)
            elif self.state == "game" and self.player:
                self.player.handle_event(event)
                
                # Обработка выхода в меню
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.state = "menu"
    
    def update(self):
        dt = self.clock.get_time() / 1000.0  # Delta time в секундах
    
        if self.state == "game" and self.player and self.level:
            # ⏰ ДОБАВЛЕНО: Получаем текущее время игры
            current_time = (pygame.time.get_ticks() - self.game_start_time) / 1000.0
        
            # 🔧 ВАЖНО: Обрабатываем непрерывный ввод клавиш
            keys = pygame.key.get_pressed()
            self.player.handle_keys(keys)  # 🔥 ДОБАВЛЕНО ЭТА СТРОКА
        
            # 🔧 Обновляем игрока
            self.player.update(
            platforms=self.level.platforms,
            enemies=self.level.enemies,
            current_time=current_time,
            traps=self.level.traps
            )
        
            # Обновление уровня
            self.level.update(dt)
        
            # Обновление камеры
            self.camera.update()
    
    def draw(self):
        # Отрисовка в зависимости от состояния
        if self.state == "menu":
            self.menu.draw(self.screen)
        elif self.state == "game":
            # Отрисовка игры
            self.level.draw(self.screen, self.camera)
            self.player.draw(self.screen, self.camera)
            self.hud.draw(self.screen)
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = RPGPlatformer()
    game.run()