import pygame
from .assets import asset_loader

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 60)
        self.hitbox = pygame.Rect(10, 10, 20, 50)
        self.velocity_y = 0
        self.speed = 5
        self.jump_power = -15
        self.gravity = 0.8
        self.is_jumping = False
        self.on_ground = False
        self.facing_right = True
        
        # Загрузка спрайтов
        # Загрузка спрайтов - добавьте отладку
        print("🔄 Loading player sprites...")
        self.idle_sprite = asset_loader.load_image("player/alienPink_stand.png", 2)
        self.current_sprite = self.idle_sprite

        # Проверка загрузки
        if self.current_sprite:
            print(f"✅ Player sprite loaded: {self.current_sprite.get_size()}")
        else:
            print("❌ Player sprite failed to load")

        # Добавляем health_component для HUD
        self.health_component = type('Health', (), {
            'current_health': 100,
            'max_health': 100
        })()

        # Добавляем experience компонент для HUD
        self.experience = type('Experience', (), {
            'current_level': 1,
            'current_exp': 0,
            'exp_to_next_level': 100
        })()

        
        # Для отладки
        self.show_hitbox = True

    def update(self, platforms):
        # Применяем гравитацию
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y
        
        # Проверка коллизий с платформами
        self.on_ground = False
        for platform in platforms:
            if self.check_collision(platform):
                if self.velocity_y > 0:  # Падение вниз
                    self.rect.bottom = platform.rect.top
                    self.on_ground = True
                    self.is_jumping = False
                elif self.velocity_y < 0:  # Движение вверх
                    self.rect.top = platform.rect.bottom
                self.velocity_y = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.on_ground:
                self.jump()

    def handle_keys(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.facing_right = False
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.facing_right = True

    def jump(self):
        if self.on_ground:
            self.velocity_y = self.jump_power
            self.is_jumping = True
            self.on_ground = False

    def check_collision(self, platform):
        player_hitbox = pygame.Rect(
            self.rect.x + self.hitbox.x,
            self.rect.y + self.hitbox.y,
            self.hitbox.width,
            self.hitbox.height
        )
        return player_hitbox.colliderect(platform.rect)

    def draw(self, screen, camera):
        """Отрисовка игрока на экране с учетом камеры"""
        # Используем offset вместо x, y
        screen_x = self.rect.x - camera.offset.x
        screen_y = self.rect.y - camera.offset.y
        print(f"🔄 Drawing player at: ({screen_x}, {screen_y}) with sprite: {self.current_sprite}")
        
        # Отрисовка спрайта
        if self.current_sprite:
            # Если персонаж смотрит влево, отражаем спрайт
            if not self.facing_right:
                flipped_sprite = pygame.transform.flip(self.current_sprite, True, False)
                screen.blit(flipped_sprite, (screen_x, screen_y))
                print("↩️  Flipped sprite")
            else:
                screen.blit(self.current_sprite, (screen_x, screen_y))
                print("➡️  Normal sprite")
        else:
            print("❌ No sprite to draw!")
            # Рисуем заглушку
            pygame.draw.rect(screen, (255, 0, 0), (screen_x, screen_y, 40, 60))
    
        # Отрисовка хитбокса (для отладки)
        if self.show_hitbox:
            hitbox_rect = pygame.Rect(
            screen_x + self.hitbox.x,
            screen_y + self.hitbox.y,
            self.hitbox.width,
            self.hitbox.height
        )
            pygame.draw.rect(screen, (255, 0, 0), hitbox_rect, 2)