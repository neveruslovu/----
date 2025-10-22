import pygame
from ..health import HealthComponent
from ..asset_loader import asset_loader

class Slime(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # Простая графика
        self.image = pygame.Surface((32, 24))
        self.image.fill((0, 255, 0))  # Зеленый квадрат
        self.rect = self.image.get_rect(topleft=(x, y))
        
        # Базовая физика
        self.health_component = HealthComponent(30)
        self.speed = 40
        self.direction = 1
        self.velocity = pygame.math.Vector2(0, 0)
        self.gravity = 1500
        
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
        """Отрисовка слайма"""
        screen.blit(self.image, camera.apply(self.rect))

    def create_animations(self):
        """Создание анимаций слайма"""
        animations = {}
    
        try:
            # Загрузка спрайт-листа слайма
            slime_img = asset_loader.load_image("enemies/slimeBlock.png", scale=2)
            if slime_img:
                # Используем один кадр для всех анимаций
                animations["idle"] = Animation([slime_img], 0.2)
                animations["move"] = Animation([slime_img], 0.15) 
                animations["attack"] = Animation([slime_img], 0.1)
                animations["hit"] = Animation([slime_img], 0.05, loop=False)
                print("✅ Загружены спрайты слайма")
                return animations
            
        except Exception as e:
            print(f"❌ Ошибка загрузки спрайтов слайма: {e}")
    
    # Заглушки если не получилось
        return self.create_placeholder_animations()