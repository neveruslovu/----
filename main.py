import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
FPS = 60
GRAVITY = 0.8
JUMP_STRENGTH = -15
PLAYER_SPEED = 5

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
LIGHT_GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 120, 255)
BROWN = (139, 69, 19)
SKY_BLUE = (135, 206, 235)
YELLOW = (255, 255, 0)
DARK_BLUE = (30, 30, 60)

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

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 50)
        self.velocity_y = 0
        self.velocity_x = 0
        self.is_jumping = False
        self.health = 100
        self.coins = 0
        self.facing_right = True
        
    def update(self, platforms):
        # Гравитация
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y
        
        # Движение по горизонтали
        self.rect.x += self.velocity_x
        
        # Проверка коллизий с платформами
        self.check_collisions(platforms)
        
        # Ограничение движения по краям экрана
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            
    def check_collisions(self, platforms):
        # Проверка коллизий с платформами
        on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                # Коллизия сверху
                if self.velocity_y > 0 and self.rect.bottom > platform.rect.top and self.rect.top < platform.rect.top:
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.is_jumping = False
                    on_ground = True
                # Коллизия снизу
                elif self.velocity_y < 0 and self.rect.top < platform.rect.bottom and self.rect.bottom > platform.rect.bottom:
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0
                # Коллизия сбоку
                elif self.velocity_x != 0:
                    if self.rect.right > platform.rect.left and self.rect.left < platform.rect.left:
                        self.rect.right = platform.rect.left
                    elif self.rect.left < platform.rect.right and self.rect.right > platform.rect.right:
                        self.rect.left = platform.rect.right
        
        # Если игрок падает ниже экрана
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.bottom = 100
            self.health -= 10
            
    def jump(self):
        if not self.is_jumping:
            self.velocity_y = JUMP_STRENGTH
            self.is_jumping = True
            
    def draw(self, screen):
        # Рисуем игрока
        color = BLUE if self.facing_right else (0, 100, 200)
        pygame.draw.rect(screen, color, self.rect)
        # Глаза
        eye_x = self.rect.right - 10 if self.facing_right else self.rect.left + 10
        pygame.draw.circle(screen, WHITE, (eye_x, self.rect.top + 15), 5)
        pygame.draw.circle(screen, BLACK, (eye_x, self.rect.top + 15), 2)

class Platform:
    def __init__(self, x, y, width, height, color=BROWN):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        # Добавляем текстуру к платформе
        pygame.draw.rect(screen, (100, 50, 0), self.rect, 2)

class Coin:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 15, 15)
        self.collected = False
        
    def draw(self, screen):
        if not self.collected:
            pygame.draw.circle(screen, YELLOW, self.rect.center, 8)
            pygame.draw.circle(screen, (200, 200, 0), self.rect.center, 6)

class Enemy:
    def __init__(self, x, y, patrol_range=100):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.speed = 2
        self.patrol_range = patrol_range
        self.start_x = x
        self.direction = 1
        self.health = 30
        
    def update(self):
        self.rect.x += self.speed * self.direction
        
        # Меняем направление при достижении границ патрулирования
        if self.rect.x > self.start_x + self.patrol_range or self.rect.x < self.start_x - self.patrol_range:
            self.direction *= -1
            
    def draw(self, screen):
        color = RED if self.direction > 0 else (200, 0, 0)
        pygame.draw.rect(screen, color, self.rect)
        # Глаза врага
        eye_x = self.rect.right - 8 if self.direction > 0 else self.rect.left + 8
        pygame.draw.circle(screen, WHITE, (eye_x, self.rect.top + 10), 4)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("RPG PLATFORMER")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "menu"
        
        # Игровые объекты
        self.player = None
        self.platforms = []
        self.coins = []
        self.enemies = []
        self.back_button = None
        
        # Создание кнопок меню
        self.buttons = self.create_menu_buttons()
        self.create_game_world()
        
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
        
    def create_game_world(self):
        # Создаем кнопку возврата в меню
        self.back_button = Button(SCREEN_WIDTH - 120, 20, 100, 40, "Меню", action=self.back_to_menu)
        
        # Создаем платформы
        self.platforms = [
            Platform(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50),  # Земля
            Platform(100, 400, 200, 20),
            Platform(400, 300, 200, 20),
            Platform(700, 400, 200, 20),
            Platform(300, 200, 150, 20),
            Platform(600, 150, 150, 20),
        ]
        
        # Создаем монеты
        self.coins = [
            Coin(150, 370),
            Coin(450, 270),
            Coin(750, 370),
            Coin(350, 170),
            Coin(650, 120),
            Coin(200, 500),
            Coin(800, 500),
        ]
        
        # Создаем врагов
        self.enemies = [
            Enemy(200, 350, 150),
            Enemy(500, 250, 100),
            Enemy(800, 350, 120),
        ]
        
    def start_game(self):
        print("Запуск новой игры")
        self.state = "game"
        # Создаем игрока
        self.player = Player(100, 300)
        
    def load_game(self):
        print("Загрузка игры")
        # Здесь будет логика загрузки игры
        
    def open_settings(self):
        print("Открытие настроек")
        self.state = "settings"
        
    def quit_game(self):
        print("Выход из игры")
        self.running = False
        
    def back_to_menu(self):
        print("Возврат в меню")
        self.state = "menu"
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            # Обработка событий мыши для кнопок
            mouse_pos = pygame.mouse.get_pos()
            
            if self.state == "menu":
                for button in self.buttons:
                    button.check_hover(mouse_pos)
                    result = button.handle_event(event)
                    if result is not None:
                        break
                        
            elif self.state == "game":
                self.back_button.check_hover(mouse_pos)
                result = self.back_button.handle_event(event)
                if result is not None:
                    return
                    
            elif self.state == "settings":
                self.back_button.check_hover(mouse_pos)
                result = self.back_button.handle_event(event)
                if result is not None:
                    return
        
        # Обработка клавиш для игрока
        if self.state == "game" and self.player:
            keys = pygame.key.get_pressed()
            self.player.velocity_x = 0
            
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.player.velocity_x = -PLAYER_SPEED
                self.player.facing_right = False
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.player.velocity_x = PLAYER_SPEED
                self.player.facing_right = True
            if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and not self.player.is_jumping:
                self.player.jump()
                
    def update_game(self):
        if self.state == "game" and self.player:
            # Обновляем игрока
            self.player.update(self.platforms)
            
            # Обновляем врагов
            for enemy in self.enemies:
                enemy.update()
                
            # Проверяем сбор монет
            for coin in self.coins:
                if not coin.collected and self.player.rect.colliderect(coin.rect):
                    coin.collected = True
                    self.player.coins += 1
                    print(f"Монет собрано: {self.player.coins}")
                    
            # Проверяем столкновение с врагами
            for enemy in self.enemies:
                if self.player.rect.colliderect(enemy.rect):
                    # Просто отталкиваем игрока
                    if self.player.rect.centerx < enemy.rect.centerx:
                        self.player.rect.right = enemy.rect.left
                    else:
                        self.player.rect.left = enemy.rect.right
                    self.player.health -= 1
                    
    def draw_menu(self):
        # Рисуем фон
        self.screen.fill(DARK_BLUE)
        
        # Рисуем заголовок
        title_font = pygame.font.Font(None, 72)
        title_text = title_font.render("RPG PLATFORMER", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title_text, title_rect)
        
        # Рисуем кнопки
        for button in self.buttons:
            button.draw(self.screen)
            
    def draw_game(self):
        # Рисуем фон (небо)
        self.screen.fill(SKY_BLUE)
        
        # Рисуем облака на заднем плане
        for i in range(5):
            x = (pygame.time.get_ticks() // 50 + i * 200) % (SCREEN_WIDTH + 200) - 100
            y = 80 + i * 40
            pygame.draw.ellipse(self.screen, WHITE, (x, y, 100, 40))
            pygame.draw.ellipse(self.screen, WHITE, (x + 25, y - 20, 80, 40))
            pygame.draw.ellipse(self.screen, WHITE, (x + 50, y, 70, 30))
        
        # Рисуем платформы
        for platform in self.platforms:
            platform.draw(self.screen)
            
        # Рисуем монеты
        for coin in self.coins:
            coin.draw(self.screen)
            
        # Рисуем врагов
        for enemy in self.enemies:
            enemy.draw(self.screen)
            
        # Рисуем игрока
        if self.player:
            self.player.draw(self.screen)
            
        # Рисуем HUD (интерфейс)
        font = pygame.font.Font(None, 36)
        health_text = font.render(f"Здоровье: {self.player.health}", True, RED)
        coins_text = font.render(f"Монеты: {self.player.coins}", True, YELLOW)
        
        self.screen.blit(health_text, (20, 20))
        self.screen.blit(coins_text, (20, 60))
        
        # Рисуем кнопку возврата в меню
        self.back_button.draw(self.screen)
    
    def draw_settings(self):
        self.screen.fill(DARK_BLUE)
        font = pygame.font.Font(None, 48)
        text = font.render("НАСТРОЙКИ", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(text, text_rect)
        
        # Инструкции
        info_font = pygame.font.Font(None, 36)
        controls = [
            "Управление:",
            "← → или A D - Движение",
            "SPACE или W - Прыжок",
            "ESC - Выход"
        ]
        
        for i, line in enumerate(controls):
            text_surface = info_font.render(line, True, WHITE)
            self.screen.blit(text_surface, (SCREEN_WIDTH // 2 - 150, 200 + i * 40))
        
        # Рисуем кнопку возврата в меню
        self.back_button.draw(self.screen)
    
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
            self.update_game()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()