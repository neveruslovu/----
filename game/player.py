"""
Класс игрока - управление, физика, анимации
"""

import pygame
import math  # ← ДОБАВЬ ЭТУ СТРОКУ
from pygame.math import Vector2
from .health import HealthComponent
from .experience import ExperienceSystem
from .items.inventory import Inventory
from .animation import Animation

class Player(pygame.sprite.Sprite):
    def __init__(self, pos=(100, 300)):
        super().__init__()
        
        # Анимации
        self.animations = self.create_animations()
        self.current_animation = "idle"
        self.facing_right = True
        
        self.image = self.animations["idle"].get_current_frame()
        self.rect = self.image.get_rect(topleft=pos)
        
        # Физика
        self.velocity = Vector2(0, 0)
        self.speed = 300
        self.jump_power = -600
        self.gravity = 1500
        self.on_ground = False
        
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
    
    def create_animations(self):
        """Создание анимаций для игрока"""
        animations = {}
        
        # Анимация покоя
        idle_frames = []
        for i in range(4):
            frame = pygame.Surface((32, 64), pygame.SRCALPHA)
            # Тело (синий комбинезон)
            pygame.draw.ellipse(frame, (30, 144, 255), (8, 20, 16, 30))  # Тело
            
            # Голова
            pygame.draw.circle(frame, (255, 218, 185), (16, 15), 8)  # Лицо
            pygame.draw.circle(frame, (0, 0, 0), (12, 13), 2)  # Левый глаз
            pygame.draw.circle(frame, (0, 0, 0), (20, 13), 2)  # Правый глаз
            
            # Рот (мимика)
            mouth_y = 18 + (i % 2)  # Легкое движение рта
            pygame.draw.arc(frame, (0, 0, 0), (13, 16, 6, 4), 0, 3.14, 1)
            
            # Волосы (каштановые)
            hair_color = (139, 69, 19)
            pygame.draw.ellipse(frame, hair_color, (8, 5, 16, 12))
            
            # Руки
            arm_sway = (i - 2) * 0.5  # Легкое покачивание рук
            pygame.draw.ellipse(frame, (30, 144, 255), (2, 25, 6, 12))  # Левая рука
            pygame.draw.ellipse(frame, (30, 144, 255), (24, 25 + arm_sway, 6, 12))  # Правая рука
            
            # Ноги
            leg_offset = (i - 1.5) * 0.8  # Легкое движение ног
            pygame.draw.ellipse(frame, (0, 0, 139), (10, 48, 5, 12))  # Левая нога
            pygame.draw.ellipse(frame, (0, 0, 139), (17, 48 + leg_offset, 5, 12))  # Правая нога
            
            idle_frames.append(frame)
        animations["idle"] = Animation(idle_frames, 0.2)
        
        # Анимация бега
        run_frames = []
        for i in range(6):
            frame = pygame.Surface((32, 64), pygame.SRCALPHA)
            
            # Тело (немного наклонено при беге)
            body_tilt = (i - 3) * 2
            pygame.draw.ellipse(frame, (30, 144, 255), (8 + body_tilt*0.2, 20, 16, 30))
            
            # Голова
            pygame.draw.circle(frame, (255, 218, 185), (16 + body_tilt*0.3, 15), 8)
            pygame.draw.circle(frame, (0, 0, 0), (12 + body_tilt*0.3, 13), 2)
            pygame.draw.circle(frame, (0, 0, 0), (20 + body_tilt*0.3, 13), 2)
            
            # Рот (открыт при беге)
            pygame.draw.arc(frame, (0, 0, 0), (13, 17, 6, 3), 0, 3.14, 1)
            
            # Волосы
            pygame.draw.ellipse(frame, (139, 69, 19), (8, 5, 16, 12))
            
            # Руки (движение при беге) - ИСПРАВЛЕННАЯ ЧАСТЬ
            arm_angle = i * 60  # 60 градусов на кадр
            arm_offset = 8 * math.sin(math.radians(arm_angle))  # ← ИСПРАВЛЕНО
            
            pygame.draw.ellipse(frame, (30, 144, 255), (2, 25 + arm_offset, 6, 12))  # Левая рука
            pygame.draw.ellipse(frame, (30, 144, 255), (24, 25 - arm_offset, 6, 12))  # Правая рука
            
            # Ноги (шагающее движение) - ИСПРАВЛЕННАЯ ЧАСТЬ
            leg_angle = i * 60
            leg_offset = 6 * math.sin(math.radians(leg_angle))  # ← ИСПРАВЛЕНО
            
            pygame.draw.ellipse(frame, (0, 0, 139), (10, 48 + leg_offset, 5, 12))  # Левая нога
            pygame.draw.ellipse(frame, (0, 0, 139), (17, 48 - leg_offset, 5, 12))  # Правая нога
            
            run_frames.append(frame)
        animations["run"] = Animation(run_frames, 0.1)
        
        # Анимация прыжка
        jump_frames = []
        for i in range(3):
            frame = pygame.Surface((32, 64), pygame.SRCALPHA)
            
            # Тело (вытянутое в прыжке)
            pygame.draw.ellipse(frame, (30, 144, 255), (8, 15, 16, 35))
            
            # Голова
            pygame.draw.circle(frame, (255, 218, 185), (16, 12), 8)
            pygame.draw.circle(frame, (0, 0, 0), (14, 10), 2)
            pygame.draw.circle(frame, (0, 0, 0), (18, 10), 2)
            
            # Рот (удивленный)
            pygame.draw.circle(frame, (0, 0, 0), (16, 15), 1)
            
            # Волосы (взлетают)
            pygame.draw.ellipse(frame, (139, 69, 19), (8, 2, 16, 12))
            
            # Руки (подняты)
            pygame.draw.ellipse(frame, (30, 144, 255), (2, 18, 6, 15))
            pygame.draw.ellipse(frame, (30, 144, 255), (24, 18, 6, 15))
            
            # Ноги (согнуты)
            pygame.draw.ellipse(frame, (0, 0, 139), (10, 48, 5, 10))
            pygame.draw.ellipse(frame, (0, 0, 139), (17, 48, 5, 10))
            
            jump_frames.append(frame)
        animations["jump"] = Animation(jump_frames, 0.15)
        
        # Анимация атаки
        attack_frames = []
        for i in range(4):
            frame = pygame.Surface((42, 64), pygame.SRCALPHA)  # Шире для атаки
            
            # Тело
            pygame.draw.ellipse(frame, (30, 144, 255), (8, 20, 16, 30))
            
            # Голова
            pygame.draw.circle(frame, (255, 218, 185), (16, 15), 8)
            pygame.draw.circle(frame, (0, 0, 0), (12, 13), 2)
            pygame.draw.circle(frame, (0, 0, 0), (20, 13), 2)
            
            # Рот (кричит при атаке)
            pygame.draw.rect(frame, (0, 0, 0), (13, 18, 6, 2))
            
            # Волосы
            pygame.draw.ellipse(frame, (139, 69, 19), (8, 5, 16, 12))
            
            # Рука с мечом
            sword_length = 15 + i * 3
            pygame.draw.ellipse(frame, (30, 144, 255), (24, 25, 6, 12))  # Рука
            pygame.draw.rect(frame, (192, 192, 192), (30, 28, sword_length, 3))  # Меч
            pygame.draw.rect(frame, (139, 0, 0), (30 + sword_length - 3, 27, 3, 5))  # Наконечник
            
            # Левая рука (защита)
            pygame.draw.ellipse(frame, (30, 144, 255), (2, 28, 6, 10))
            
            # Ноги (стойка боя)
            pygame.draw.ellipse(frame, (0, 0, 139), (10, 48, 5, 12))
            pygame.draw.ellipse(frame, (0, 0, 139), (17, 50, 5, 10))
            
            attack_frames.append(frame)
        animations["attack"] = Animation(attack_frames, 0.08, loop=False)
        
        # Анимация получения урона
        hit_frames = []
        for i in range(3):
            frame = pygame.Surface((32, 64), pygame.SRCALPHA)
            
            # Тело (красное при уроне)
            body_color = (255, 100, 100) if i % 2 == 0 else (30, 144, 255)
            pygame.draw.ellipse(frame, body_color, (8, 20, 16, 30))
            
            # Голова
            pygame.draw.circle(frame, (255, 218, 185), (16, 15), 8)
            pygame.draw.circle(frame, (0, 0, 0), (12, 13), 2)
            pygame.draw.circle(frame, (0, 0, 0), (20, 13), 2)
            
            # Рот (боль)
            pygame.draw.arc(frame, (0, 0, 0), (13, 17, 6, 3), 3.14, 6.28, 1)
            
            # Волосы
            pygame.draw.ellipse(frame, (139, 69, 19), (8, 5, 16, 12))
            
            # Руки
            pygame.draw.ellipse(frame, body_color, (2, 25, 6, 12))
            pygame.draw.ellipse(frame, body_color, (24, 25, 6, 12))
            
            # Ноги
            pygame.draw.ellipse(frame, (0, 0, 139), (10, 48, 5, 12))
            pygame.draw.ellipse(frame, (0, 0, 139), (17, 48, 5, 12))
            
            hit_frames.append(frame)
        animations["hit"] = Animation(hit_frames, 0.1, loop=False)
        
        return animations
    
    def update_animation(self, dt):
        """Обновление текущей анимации"""
        self.animations[self.current_animation].update(dt)
        
        # Автоматическое переключение анимаций
        if self.damage_effect_timer > 0:
            self.current_animation = "hit"
        elif self.is_attacking:
            self.current_animation = "attack"
            if self.animations["attack"].done:
                self.is_attacking = False
        elif not self.on_ground:
            self.current_animation = "jump"
        elif abs(self.velocity.x) > 0:
            self.current_animation = "run"
        else:
            self.current_animation = "idle"
        
        # Получение текущего кадра
        self.image = self.animations[self.current_animation].get_current_frame()
        
        # Отражение спрайта при смене направления
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)
    
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
        self.attack_cooldown = 0.3
        self.animations["attack"].reset()
        
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
    
    def handle_collisions(self, level):
        """Обработка столкновений с уровнем"""
        self.on_ground = False
        
        for platform in level.platforms:
            if self.rect.colliderect(platform.rect):
                self.resolve_collision(platform.rect)
    
    def resolve_collision(self, platform_rect):
        """Разрешение столкновения с платформой"""
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
            if dx < 0:
                self.rect.right = platform_rect.left
            else:
                self.rect.left = platform_rect.right
    
    def take_damage(self, amount):
        """Игрок получает урон"""
        damaged = self.health_component.take_damage(amount)
        if damaged:
            print(f"💔 Игрок получил {amount} урона! HP: {self.health_component.current_health}")
            self.damage_effect_timer = 0.3
            self.animations["hit"].reset()
        return damaged
    
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
        
        # Обновление анимации
        self.update_animation(dt)
        
        # Обновление эффектов
        if self.damage_effect_timer > 0:
            self.damage_effect_timer -= dt
        
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
    
    def draw(self, screen, camera):
        """Отрисовка игрока"""
        screen.blit(self.image, camera.apply(self.rect))
        
        # Отладочная отрисовка хитбокса атаки
        if self.is_attacking:
            attack_pos = camera.apply(self.attack_rect)
            pygame.draw.rect(screen, (255, 255, 0), attack_pos, 2)