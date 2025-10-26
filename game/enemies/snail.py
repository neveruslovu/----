# game/enemies/snail.py
import pygame
from ..asset_loader import asset_loader

class Snail(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # Загрузка спрайта
        try:
            self.image = asset_loader.load_image("enemies/snail.png", 1)
        except:
            # Заглушка если спрайт не загрузился
            self.image = pygame.Surface((40, 30))
            self.image.fill((150, 75, 0))  # Коричневый цвет
        
        self.rect = self.image.get_rect(topleft=(x, y))
        
        # Физика и AI
        self.speed = 40  # Улитки медленнее слаймов
        self.direction = 1
        self.velocity = pygame.math.Vector2(0, 0)
        self.gravity = 1500
        self.facing_right = True
        
        # Хитбокс
        self.hitbox = pygame.Rect(0, 0, 30, 25)
        self.show_hitbox = True
        
        print(f"🐌 Улитка создана на позиции ({x}, {y})!")
    
    def update(self, dt, level):
        """Обновление улитки"""
        # Движение по горизонтали
        self.velocity.x = self.speed * self.direction
        self.velocity.y += self.gravity * dt
        
        # Применяем движение
        self.rect.x += self.velocity.x * dt
        self.rect.y += self.velocity.y * dt
        
        # Обновляем направление
        if self.velocity.x > 0:
            self.facing_right = True
        elif self.velocity.x < 0:
            self.facing_right = False
        
        ground_level = level.height - 100  # 100px от нижнего края уровня
        if self.rect.bottom > ground_level:
            self.rect.bottom = ground_level
            self.velocity.y = 0
        
            # Меняем направление при достижении края уровня
            level_width = level.width
            if self.rect.right > level_width - 100 or self.rect.left < 100:
                self.direction *= -1

            
    
    def draw(self, screen, camera):
        """Отрисовка улитки"""
        screen_rect = self.rect.move(-camera.offset.x, -camera.offset.y)
        
        # Отрисовка спрайта
        if not self.facing_right:
            flipped_sprite = pygame.transform.flip(self.image, True, False)
            screen.blit(flipped_sprite, screen_rect)
        else:
            screen.blit(self.image, screen_rect)
        
        # Отрисовка хитбокса (для отладки)
        if self.show_hitbox:
            hitbox_rect = pygame.Rect(
                screen_rect.x + self.hitbox.x,
                screen_rect.y + self.hitbox.y,
                self.hitbox.width,
                self.hitbox.height
            )
            pygame.draw.rect(screen, (255, 0, 0), hitbox_rect, 2)