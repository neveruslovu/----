import pygame
import sys
import os

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
LIGHT_GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Button:
    def __init__(self, x, y, width, height, text, color=GRAY, hover_color=LIGHT_GRAY, text_color=WHITE, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.action = action
        self.is_hovered = False
        self.font = pygame.font.Font(None, 36)
        
    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=10)
        
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered and self.action:
                return self.action()
        return None

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("RPG PLATFORMER")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "menu"
        
        # Загрузка фона
        self.background = self.load_background()
        
        # Создание кнопок меню
        self.buttons = self.create_menu_buttons()
        
    def load_background(self):
        # Создаем простой фон если нет изображения
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        background.fill((30, 30, 60))  # Темно-синий фон
        return background
        
    def create_menu_buttons(self):
        button_width = 300
        button_height = 60
        button_x = SCREEN_WIDTH // 2 - button_width // 2
        start_y = SCREEN_HEIGHT // 2 - 100
        
        buttons = [
            Button(button_x, start_y, button_width, button_height, "Новая игра", action=self.start_game),
            Button(button_x, start_y + 80, button_width, button_height, "Загрузить", action=self.load_game),
            Button(button_x, start_y + 160, button_width, button_height, "Настройки", action=self.open_settings),
            Button(button_x, start_y + 240, button_width, button_height, "Выход", action=self.quit_game)
        ]
        
        return buttons
        
    def start_game(self):
        print("Запуск новой игры")
        self.state = "game"
        # Здесь будет логика начала новой игры
        
    def load_game(self):
        print("Загрузка игры")
        # Здесь будет логика загрузки игры
        
    def open_settings(self):
        print("Открытие настроек")
        self.state = "settings"
        # Здесь будет логика открытия настроек
        
    def quit_game(self):
        print("Выход из игры")
        self.running = False
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            # Обработка событий мыши для кнопок
            if self.state == "menu":
                mouse_pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    button.check_hover(mouse_pos)
                    result = button.handle_event(event)
                    if result is not None:
                        break
                        
    def draw_menu(self):
        # Рисуем фон
        self.screen.blit(self.background, (0, 0))
        
        # Рисуем заголовок
        title_font = pygame.font.Font(None, 72)
        title_text = title_font.render("RPG PLATFORMER", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title_text, title_rect)
        
        # Рисуем кнопки
        for button in self.buttons:
            button.draw(self.screen)
            
    def draw_game(self):
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 48)
        text = font.render("ИГРА ЗАПУЩЕНА", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text, text_rect)
        
        # Кнопка возврата в меню
        back_button = Button(SCREEN_WIDTH - 150, 50, 120, 40, "Меню", action=self.back_to_menu)
        mouse_pos = pygame.mouse.get_pos()
        back_button.check_hover(mouse_pos)
        back_button.draw(self.screen)
        
        # Обработка кнопки возврата
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_button.rect.collidepoint(event.pos):
                    self.back_to_menu()
    
    def draw_settings(self):
        self.screen.fill((0, 0, 50))
        font = pygame.font.Font(None, 48)
        text = font.render("НАСТРОЙКИ", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(text, text_rect)
        
        # Кнопка возврата в меню
        back_button = Button(SCREEN_WIDTH - 150, 50, 120, 40, "Меню", action=self.back_to_menu)
        mouse_pos = pygame.mouse.get_pos()
        back_button.check_hover(mouse_pos)
        back_button.draw(self.screen)
        
        # Обработка кнопки возврата
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_button.rect.collidepoint(event.pos):
                    self.back_to_menu()
    
    def back_to_menu(self):
        self.state = "menu"
    
    def draw(self):
        if self.state == "menu":
            self.draw_menu()
        elif self.state == "game":
            self.draw_game()
        elif self.state == "settings":
            self.draw_settings()
            
        pygame.display.flip()
        
    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()