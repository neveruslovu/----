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
from .asset_loader import asset_loader

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
        """Создание анимаций из отдельных файлов Kenney"""
        animations = {}
        
        try:
            # ПРОСТОЙ ВАРИАНТ - загружаем каждую анимацию как один кадр
            # Idle анимация
            idle_img = asset_loader.load_image("player/player_idle.png", scale=2)
            if idle_img:
                animations["idle"] = Animation([idle_img], 0.2)
                print("✅ Загружена idle анимация")
            else:
                print("❌ Не удалось загрузить idle анимацию")

            # Run анимация  
            run_img = asset_loader.load_image("player/player_run.png", scale=2)
            if run_img:
                animations["run"] = Animation([run_img], 0.15)
                print("✅ Загружена run анимация")
            else:
                print("❌ Не удалось загрузить run анимацию")

            # Jump анимация
            jump_img = asset_loader.load_image("player/player_jump.png", scale=2)
            if jump_img:
                animations["jump"] = Animation([jump_img], 0.2)
                print("✅ Загружена jump анимация")
            else:
                print("❌ Не удалось загрузить jump анимацию")

            # Hit анимация (если есть файл)
            try:
                hit_img = asset_loader.load_image("player/player_hit.png", scale=2)
                if hit_img:
                    animations["hit"] = Animation([hit_img], 0.1, loop=False)
                    print("✅ Загружена hit анимация")
            except:
                print("ℹ️ Файл hit анимации не найден, создам заглушку")
                hit_frame = pygame.Surface((32, 64), pygame.SRCALPHA)
                hit_frame.fill((255, 100, 100))
                animations["hit"] = Animation([hit_frame], 0.1, loop=False)

            # Проверяем что загрузилось хотя бы одна анимация
            if animations:
                print("🎉 Анимации игрока загружены!")
                return animations
            else:
                print("❌ Не удалось загрузить ни одну анимацию игрока")
                return self.create_placeholder_animations()
                
        except Exception as e:
            print(f"❌ Ошибка загрузки спрайтов: {e}")
            import traceback
            traceback.print_exc()
            return self.create_placeholder_animations()
    
    def create_placeholder_animations(self):
        """Анимации-заглушки на случай отсутствия спрайтов"""
        animations = {}
        
        # Idle анимация
        idle_frames = []
        for i in range(4):
            frame = pygame.Surface((32, 64), pygame.SRCALPHA)
            # Синий игрок
            pygame.draw.ellipse(frame, (30, 144, 255), (8, 20, 16, 30))
            pygame.draw.circle(frame, (255, 218, 185), (16, 15), 8)
            pygame.draw.circle(frame, (0, 0, 0), (12, 13), 2)
            pygame.draw.circle(frame, (0, 0, 0), (20, 13), 2)
            idle_frames.append(frame)
        animations["idle"] = Animation(idle_frames, 0.2)
        
        # Run анимация
        run_frames = []
        for i in range(6):
            frame = pygame.Surface((32, 64), pygame.SRCALPHA)
            color = (0, 255, 0) if i % 2 == 0 else (30, 144, 255)
            pygame.draw.ellipse(frame, color, (8, 20, 16, 30))
            run_frames.append(frame)
        animations["run"] = Animation(run_frames, 0.1)
        
        return animations

    # ... остальные методы класса (update, handle_input и т.д.)