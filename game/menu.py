import pygame

class MainMenu:
    def __init__(self, app):
        self.app = app
        self.options = ["Новая игра", "Загрузить", "Настройки", "Выход"]
        self.selected_index = 0
        self.font = pygame.font.Font(None, 48)
        self.title_font = pygame.font.Font(None, 72)
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.options)
            elif event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                self.select_option()
    
    def select_option(self):
        option = self.options[self.selected_index]
        if option == "Новая игра":
            self.app.start_game()
        elif option == "Выход":
            self.app.running = False
    
    def update(self, dt):
        pass
    
    def draw(self, screen):
        screen.fill((30, 30, 60))
        
        # Заголовок
        title = self.title_font.render("RPG PLATFORMER", True, (255, 255, 255))
        screen.blit(title, (screen.get_width()//2 - title.get_width()//2, 100))
        
        # Опции
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected_index else (255, 255, 255)
            text = self.font.render(option, True, color)
            screen.blit(text, (screen.get_width()//2 - text.get_width()//2, 250 + i * 60))