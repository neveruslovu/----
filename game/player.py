import pygame
from .asset_loader import asset_loader

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
        
        print(f"🎯 Player created at position: ({x}, {y})")
        
        # Загрузка спрайтов
        self.idle_sprite = asset_loader.load_image("player/alienPink_stand.png", 2)
        self.current_sprite = self.idle_sprite
        
        # Компоненты для HUD
        self.health_component = type('Health', (), {
            'current_health': 100,
            'max_health': 100
        })()
        
        self.experience = type('Experience', (), {
            'current_level': 1,
            'current_exp': 0,
            'exp_to_next_level': 100
        })()
        
        self.show_hitbox = True

    def update(self, platforms):
        """Обновление состояния игрока"""
        print(f"🔄 Player update - Position: ({self.rect.x}, {self.rect.y}), Velocity: {self.velocity_y}, On ground: {self.on_ground}")
        
        # Применяем гравитацию
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y
        
        print(f"📉 After gravity - Position: ({self.rect.x}, {self.rect.y}), Velocity: {self.velocity_y}")
        
        # Проверка коллизий с платформами
        self.on_ground = False
        collision_count = 0
        
        for platform in platforms:
            if self.check_collision(platform):
                collision_count += 1
                if self.velocity_y > 0:  # Падение вниз
                    self.rect.bottom = platform.rect.top
                    self.on_ground = True
                    self.is_jumping = False
                    self.velocity_y = 0
                    print("👆 Landed on platform")
                elif self.velocity_y < 0:  # Движение вверх
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0
                    print("👇 Hit platform from below")
        
        print(f"📊 Collisions detected: {collision_count}, On ground: {self.on_ground}")

    def handle_event(self, event):
        """Обработка одиночных событий"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.on_ground:
                self.jump()
                print("🦘 Jump!")

    def handle_keys(self, keys):
        """Обработка непрерывного ввода клавиш"""
        moved = False
    
        # Проверяем все возможные клавиши движения
        arrow_left = keys[pygame.K_LEFT] 
        arrow_right = keys[pygame.K_RIGHT]
        a_key = keys[pygame.K_a]  # Альтернативная клавиша A
        d_key = keys[pygame.K_d]  # Альтернативная клавиша D
    
        if arrow_left or a_key:
            self.rect.x -= self.speed
            self.facing_right = False
            moved = True
            print(f"⬅️  Moving LEFT (Arrow: {arrow_left}, A: {a_key})")
        if arrow_right or d_key:
            self.rect.x += self.speed
            self.facing_right = True
            moved = True
            print(f"➡️  Moving RIGHT (Arrow: {arrow_right}, D: {d_key})")
    
        if moved:
            print(f"🎯 New position: ({self.rect.x}, {self.rect.y})")

        else:
            print("⏸️  No movement keys pressed")

    def jump(self):
        """Прыжок игрока"""
        if self.on_ground:
            self.velocity_y = self.jump_power
            self.is_jumping = True
            self.on_ground = False
            print(f"🚀 Jump! Velocity: {self.velocity_y}")

    def check_collision(self, platform):
        """Проверка коллизии с платформой"""
        player_hitbox = pygame.Rect(
            self.rect.x + self.hitbox.x,
            self.rect.y + self.hitbox.y,
            self.hitbox.width,
            self.hitbox.height
        )
        return player_hitbox.colliderect(platform.rect)

    def draw(self, screen, camera):
        """Отрисовка игрока"""
        screen_x = self.rect.x - camera.offset.x
        screen_y = self.rect.y - camera.offset.y
        
        print(f"🎨 Drawing player at screen: ({screen_x}, {screen_y}), world: ({self.rect.x}, {self.rect.y})")
        
        # Отрисовка спрайта
        if self.current_sprite:
            if not self.facing_right:
                flipped_sprite = pygame.transform.flip(self.current_sprite, True, False)
                screen.blit(flipped_sprite, (screen_x, screen_y))
            else:
                screen.blit(self.current_sprite, (screen_x, screen_y))
        else:
            # Заглушка если спрайт не загружен
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