import pygame
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

class HUD:
    def __init__(self, player):
        self.player = player
        self.font = pygame.font.Font(None, 36)
        
        # 🔧 СНАЧАЛА объявляем heart_size
        self.heart_size = 30  # Размер сердечек
        
        # 🔧 ПОТОМ загружаем спрайты сердец
        self.heart_full = self.load_heart_image("hud/hudheart_full.png")
        self.heart_half = self.load_heart_image("hud/hudheart_half.png") 
        self.heart_empty = self.load_heart_image("hud/hudheart_empty.png")
        
        print("🎯 HUD с сердцами инициализирован")
    
    def load_heart_image(self, path):
        """Загружает изображение сердца с масштабированием"""
        try:
            from game.asset_loader import asset_loader
            heart = asset_loader.load_image(path, 1.0)
            if heart:
                # Масштабируем до нужного размера
                return pygame.transform.scale(heart, (self.heart_size, self.heart_size))
        except Exception as e:
            print(f"❌ Не удалось загрузить {path}: {e}")
        
        # Заглушка если изображение не загрузилось
        surface = pygame.Surface((self.heart_size, self.heart_size), pygame.SRCALPHA)
        pygame.draw.rect(surface, (255, 0, 0), (0, 0, self.heart_size, self.heart_size))
        return surface
    
    def draw(self, screen):
        """Отрисовка HUD с сердцами"""
        try:
            # 🔥 ИСПРАВЛЕНИЕ: Получаем здоровье напрямую из health_component игрока
            if hasattr(self.player, 'health_component'):
                # Предполагаем, что health_component имеет current_health и max_health
                current_health = self.player.health_component.current_health
                max_health = self.player.health_component.max_health
            else:
                # 🔥 РЕЗЕРВНАЯ ЛОГИКА: если health_component нет, используем значения по умолчанию
                current_health = 100
                max_health = 100
                print("⚠️ HealthComponent не найден, используем значения по умолчанию")
            
            # 🔧 ОТРИСОВКА СЕРДЕЦ
            self.draw_hearts(screen, current_health, max_health)
            
            # 🔥 ДОПОЛНИТЕЛЬНО: отображаем числовое значение HP для отладки
            hp_text = f"HP: {current_health}/{max_health}"
            hp_surface = self.font.render(hp_text, True, (255, 255, 255))
            screen.blit(hp_surface, (10, 50))
            
            # 🔥 ОТОБРАЖЕНИЕ СОСТОЯНИЯ ИГРОКА (жив/мертв)
            if hasattr(self.player, 'is_alive') and not self.player.is_alive:
                death_text = self.font.render("DEAD - Respawning...", True, (255, 0, 0))
                screen.blit(death_text, (10, 90))
            
            # 🔥 ОТОБРАЖЕНИЕ НЕУЯЗВИМОСТИ
            if hasattr(self.player, 'is_invincible') and self.player.is_invincible:
                invincible_text = self.font.render("INVINCIBLE", True, (0, 255, 255))
                screen.blit(invincible_text, (10, 130))
                
        except Exception as e:
            print(f"❌ HUD error: {e}")
            # Минимальный HUD при ошибках
            error_text = self.font.render("HUD ERROR", True, (255, 0, 0))
            screen.blit(error_text, (10, 10))
    
    def draw_hearts(self, screen, current_health, max_health):
        """Отрисовка системы сердец"""
        hearts_count = max_health // 20  # Каждое сердце = 20 HP
        health_per_heart = 20
        
        x_position = 10
        y_position = 10
        
        for i in range(hearts_count):
            heart_health = current_health - (i * health_per_heart)
            
            if heart_health >= health_per_heart:
                # Полное сердце
                screen.blit(self.heart_full, (x_position, y_position))
            elif heart_health >= health_per_heart // 2:
                # Полусердце
                screen.blit(self.heart_half, (x_position, y_position))
            elif heart_health > 0:
                # Полусердце (меньше половины)
                screen.blit(self.heart_half, (x_position, y_position))
            else:
                # Пустое сердце
                screen.blit(self.heart_empty, (x_position, y_position))
            
            x_position += self.heart_size + 5  # Расстояние между сердцами