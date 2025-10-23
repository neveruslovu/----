import pygame
from ..health import HealthComponent
from ..asset_loader import asset_loader

class Slime(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        self.idle_sprite = asset_loader.load_image("enemies/slimePurple.png", 0.4)
        self.current_sprite = self.idle_sprite
    
        # Графика - используем загруженный спрайт
        if self.current_sprite:
            self.image = self.current_sprite
            self.rect = self.image.get_rect(topleft=(x, y))
            # Хитбокс относительно РЕАЛЬНОГО размера спрайта
            sprite_width, sprite_height = self.image.get_size()
            self.hitbox = pygame.Rect(
                (sprite_width -20 ) // 2,  # Центрируем по горизонтали
                (sprite_height +13) // 2, # Центрируем по вертикали
                22, 22
            )
        else:
            self.image = pygame.Surface((34, 24))
            self.rect = self.image.get_rect(topleft=(x, y))
            self.hitbox = pygame.Rect(10, 10, 20, 20)
        

        self.show_hitbox = True
        

        # Базовая физика
        self.health_component = HealthComponent(30)
        self.speed = 40
        self.direction = 1
        self.velocity = pygame.math.Vector2(0, 0)
        self.gravity = 1500
        self.facing_right = True
        
        print(f"🐌 Слайм создан на позиции ({x}, {y})!")
    
    def update(self, dt, level):
        """Простое обновление слайма"""
        # Простое движение туда-сюда
        self.velocity.x = self.speed * self.direction
        self.velocity.y += self.gravity * dt
        
        # Движение
        self.rect.x += self.velocity.x * dt
        self.rect.y += self.velocity.y * dt
        
        # Простая проверка столкновений с землей
        if self.rect.bottom > 500:  # Высота земли
            self.rect.bottom = 500
            self.velocity.y = 0
            
            # Меняем направление при достижении края
            if self.rect.right > 700 or self.rect.left < 100:
                self.direction *= -1
        
        # Обновление здоровья
        self.health_component.update(dt)
        
        # Проверка смерти
        if self.health_component.is_dead():
            self.kill()
    
    def take_damage(self, amount):
        """Получение урона"""
        damaged = self.health_component.take_damage(amount)
        if damaged:
            print(f"💥 Слайм получил {amount} урона!")
            # Мигание красным
            self.image.fill((255, 0, 0))
            pygame.time.set_timer(pygame.USEREVENT + 2, 200)  # Вернем цвет через 200ms
        return damaged
    
    def draw(self, screen, camera):
        """Отрисовка slimes"""
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