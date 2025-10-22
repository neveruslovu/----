"""
Класс игрока - управление, физика, анимации
"""

import pygame
from pygame.math import Vector2
from .health import HealthComponent
from .experience import ExperienceSystem
from .items.inventory import Inventory

class Player(pygame.sprite.Sprite):
    def __init__(self, pos=(100, 300)):
        super().__init__()
        
        # Позиция и размеры
        self.image = pygame.Surface((32, 64))
        self.image.fill((255, 0, 0))  # Красный квадрат как заглушка
        self.rect = self.image.get_rect(topleft=pos)
        
        # Физика
        self.velocity = Vector2(0, 0)
        self.speed = 300
        self.jump_power = -600
        self.gravity = 1500
        self.on_ground = False
        self.facing_right = True
        
        # Боевая система
        self.is_attacking = False
        self.attack_cooldown = 0
        self.attack_damage = 10
        self.attack_rect = pygame.Rect(0, 0, 50, 32)
        
        # RPG системы
        self.health_component = HealthComponent(100)
        self.experience = ExperienceSystem(self)
        self.inventory = Inventory()
        
        # Таймер для эффектов
        self.damage_effect_timer = 0
        
        print("🎯 Игрок создан!")
    
    def handle_input(self):
        """Обработка ввода игрока"""
        keys = pygame.key.get_pressed()
        
        # Горизонтальное движение
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.velocity.x = -self.speed
            self.facing_right = False
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.velocity.x = self.speed
            self.facing_right = True
        else:
            self.velocity.x = 0
            
        # Прыжок
        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
            self.jump()
            
        # Атака
        if keys[pygame.K_j] and not self.is_attacking and self.attack_cooldown <= 0:
            self.attack()
    
    def jump(self):
        """Прыжок игрока"""
        self.velocity.y = self.jump_power
        self.on_ground = False
        print("🦘 Прыжок!")
    
    def attack(self):
        """Атака игрока"""
        self.is_attacking = True
        self.attack_cooldown = 0.3  # 300ms кд
        
        # Позиционирование хитбокса атаки
        if self.facing_right:
            self.attack_rect.midleft = self.rect.midright
        else:
            self.attack_rect.midright = self.rect.midleft
            
        print("⚔️ Атака!")
    
    def apply_physics(self, dt):
        """Применение физики"""
        # Гравитация
        self.velocity.y += self.gravity * dt
        
        # Ограничение скорости падения
        if self.velocity.y > 1000:
            self.velocity.y = 1000
            
        # Кд атаки
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt
            if self.attack_cooldown <= 0:
                self.is_attacking = False
    
    def handle_collisions(self, level):
        """Обработка столкновений с уровнем"""
        self.on_ground = False
        
        for platform in level.platforms:
            if self.rect.colliderect(platform.rect):
                self.resolve_collision(platform.rect)
    
    def resolve_collision(self, platform_rect):
        """Разрешение столкновения с платформой"""
        # Определяем направление столкновения
        dx = (self.rect.centerx - platform_rect.centerx) / (platform_rect.width / 2)
        dy = (self.rect.centery - platform_rect.centery) / (platform_rect.height / 2)
        
        # Столкновение сверху
        if abs(dy) > abs(dx) and dy < 0 and self.velocity.y > 0:
            self.rect.bottom = platform_rect.top
            self.velocity.y = 0
            self.on_ground = True
        # Столкновение снизу
        elif abs(dy) > abs(dx) and dy > 0 and self.velocity.y < 0:
            self.rect.top = platform_rect.bottom
            self.velocity.y = 0
        # Столкновение сбоку
        elif abs(dx) > abs(dy):
            if dx < 0:  # Слева
                self.rect.right = platform_rect.left
            else:  # Справа
                self.rect.left = platform_rect.right
    
    def take_damage(self, amount):
        """Игрок получает урон"""
        damaged = self.health_component.take_damage(amount)
        if damaged:
            print(f"💔 Игрок получил {amount} урона! HP: {self.health_component.current_health}")
            
            # Эффект получения урона
            self.damage_effect_timer = 0.3  # 300ms эффект
            self.image.fill((255, 100, 100))  # Красный цвет при получении урона
            
        return damaged
    
    def update_visuals(self):
        """Обновление визуального состояния игрока"""
        if self.damage_effect_timer > 0:
            # Мигание при получении урона
            import time
            blink = int(time.time() * 10) % 2
            if blink == 0:
                self.image.fill((255, 100, 100))  # Красный
            else:
                if self.velocity.x != 0:
                    self.image.fill((0, 255, 0))  # Зеленый при движении
                else:
                    self.image.fill((255, 0, 0))  # Красный при стоянии
        else:
            # Нормальные цвета
            if self.velocity.x != 0:
                self.image.fill((0, 255, 0))  # Зеленый при движении
            else:
                self.image.fill((255, 0, 0))  # Красный при стоянии
    
    def update(self, dt, level):
        """Обновление состояния игрока"""
        self.handle_input()
        self.apply_physics(dt)
        
        # Движение
        self.rect.x += self.velocity.x * dt
        self.rect.y += self.velocity.y * dt
        
        # Коллизии
        self.handle_collisions(level)
        
        # Обновление здоровья
        self.health_component.update(dt)
        
        # Обновление визуальных эффектов
        if self.damage_effect_timer > 0:
            self.damage_effect_timer -= dt
        self.update_visuals()
        
        # Проверка смерти
        if self.health_component.is_dead():
            self.respawn()
    
    def respawn(self):
        """Возрождение игрока после смерти"""
        print("💀 Игрок умер! Возрождение...")
        self.health_component.current_health = self.health_component.max_health
        self.rect.topleft = (100, 300)
        self.velocity = Vector2(0, 0)
        self.damage_effect_timer = 0
        self.update_visuals()  # Возвращаем нормальный цвет
    
    def draw(self, screen, camera):
        """Отрисовка игрока"""
        screen.blit(self.image, camera.apply(self.rect))
        
        # Отладочная отрисовка хитбокса атаки
        if self.is_attacking:
            attack_pos = camera.apply(self.attack_rect)
            pygame.draw.rect(screen, (255, 255, 0), attack_pos, 2)