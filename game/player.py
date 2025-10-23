import pygame
from .asset_loader import asset_loader

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 50)
        self.hitbox = pygame.Rect(10, 10, 20, 45)
        self.velocity_y = 0
        self.speed = 5
        self.jump_power = -15
        self.gravity = 0.8
        self.is_jumping = False
        self.on_ground = False
        self.facing_right = True
        
        # 🔧 УЛУЧШЕНИЕ: Coyote Time переменные
        self.coyote_time = 0.15  # 150ms окно для прыжка после схода с платформы
        self.time_since_ground = 0
        self.jump_buffer = 0     # Буфер ввода прыжка
        self.jump_buffer_time = 0.1  # 100ms буфер
        
        print(f"🎯 Player created at position: ({x}, {y})")
        
        # Загрузка спрайтов
        self.idle_sprite = asset_loader.load_image("player/alienPink_stand.png", 0.3)
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
        """Обновление состояния игрока с улучшенной физикой"""
        # Сохраняем состояние до обновления
        was_on_ground = self.on_ground
        
        # Применяем гравитацию
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y
        
        # 🔧 УЛУЧШЕНИЕ: Обновляем таймеры
        if self.jump_buffer > 0:
            self.jump_buffer -= 1/60  # Уменьшаем буфер
        
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
                    self.time_since_ground = 0  # 🔧 Сбрасываем таймер
                elif self.velocity_y < 0:  # Движение вверх
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0
        
        # 🔧 УЛУЧШЕНИЕ: Обновляем Coyote Time
        if self.on_ground:
            self.time_since_ground = 0
        elif was_on_ground:
            # Только что оторвались от земли
            self.time_since_ground = 0
        else:
            # В воздухе - увеличиваем таймер
            self.time_since_ground += 1/60  # ~16.67ms за кадр
        
        # 🔧 УЛУЧШЕНИЕ: Автопрыжок по буферу
        if self.jump_buffer > 0 and self.can_jump():
            self.jump()
            self.jump_buffer = 0

    def handle_event(self, event):
        """Обработка одиночных событий"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # 🔧 УЛУЧШЕНИЕ: Сохраняем ввод в буфер вместо немедленного прыжка
                self.jump_buffer = self.jump_buffer_time
                print("💾 Jump input buffered")

    def handle_keys(self, keys):
        """Обработка непрерывного ввода клавиш"""
        moved = False
    
        arrow_left = keys[pygame.K_LEFT] 
        arrow_right = keys[pygame.K_RIGHT]
        a_key = keys[pygame.K_a]
        d_key = keys[pygame.K_d]
    
        if arrow_left or a_key:
            self.rect.x -= self.speed
            self.facing_right = False
            moved = True
        if arrow_right or d_key:
            self.rect.x += self.speed
            self.facing_right = True
            moved = True

    def can_jump(self):
        """🔧 УЛУЧШЕНИЕ: Проверяет, может ли игрок прыгнуть"""
        return (self.on_ground or 
                self.time_since_ground < self.coyote_time) and not self.is_jumping

    def jump(self):
        """🔧 УЛУЧШЕНИЕ: Умный прыжок с Coyote Time"""
        if self.can_jump():
            self.velocity_y = self.jump_power
            self.is_jumping = True
            self.on_ground = False
            self.time_since_ground = self.coyote_time  # Предотвращаем повторные прыжки
            print(f"🚀 Jump! Velocity: {self.velocity_y}, Coyote: {self.time_since_ground:.2f}")

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
        
        # Отрисовка спрайта
        if self.current_sprite:
            if not self.facing_right:
                flipped_sprite = pygame.transform.flip(self.current_sprite, True, False)
                screen.blit(flipped_sprite, (screen_x, screen_y))
            else:
                screen.blit(self.current_sprite, (screen_x, screen_y))
        else:
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
            