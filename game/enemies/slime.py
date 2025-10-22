import pygame
from ..health import HealthComponent

class Slime(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((32, 24))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(topleft=(x, y))
        
        self.health_component = HealthComponent(30)
        self.speed = 50
        self.direction = 1
        self.velocity = pygame.math.Vector2(0, 0)
        self.gravity = 1500
        
    def update(self, dt, level):
        self.velocity.x = self.speed * self.direction
        self.velocity.y += self.gravity * dt
        
        self.rect.x += self.velocity.x * dt
        self.rect.y += self.velocity.y * dt
        
        self.handle_collisions(level)
        
        if not self.check_forward_platform(level):
            self.direction *= -1
        
        self.health_component.update(dt)
        
        if self.health_component.is_dead():
            self.kill()
    
    def handle_collisions(self, level):
        for platform in level.platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity.y > 0 and self.rect.bottom > platform.rect.top:
                    self.rect.bottom = platform.rect.top
                    self.velocity.y = 0
    
    def check_forward_platform(self, level):
        check_rect = self.rect.copy()
        check_rect.x += self.direction * 10
        check_rect.y += 5
        
        for platform in level.platforms:
            if check_rect.colliderect(platform.rect):
                return True
        return False
    
    def take_damage(self, amount):
        damaged = self.health_component.take_damage(amount)
        if damaged:
            self.image.fill((255, 0, 0))  # Красный при получении урона
        return damaged
    
    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self.rect))