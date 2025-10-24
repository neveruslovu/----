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
            
                       
            # 🔥 ОТОБРАЖЕНИЕ СОСТОЯНИЯ ИГРОКА (жив/мертв)
            if hasattr(self.player, 'is_alive') and not self.player.is_alive:
                # 🔥 КРАСИВАЯ НАДПИСЬ СМЕРТИ ПО ЦЕНТРУ
                screen_width, screen_height = screen.get_size()
    
                # Создаем большой шрифт для основной надписи
                death_font_large = pygame.font.Font(None, 72)  # Большой шрифт
                death_font_small = pygame.font.Font(None, 36)  # Меньший шрифт
    
                # Основная надпись "ВЫ УМЕРЛИ"
                death_text = death_font_large.render("ВЫ УМЕРЛИ", True, (255, 0, 0))
                death_rect = death_text.get_rect(center=(screen_width // 2, screen_height // 2 - 30))
    
                # Вторая надпись "Возрождение..."
                respawn_text = death_font_small.render("Возрождение...", True, (255, 255, 255))
                respawn_rect = respawn_text.get_rect(center=(screen_width // 2, screen_height // 2 + 30))
    
                # 🔥 ДОБАВЛЯЕМ ЭФФЕКТ ПУЛЬСАЦИИ
                pulse = abs(pygame.time.get_ticks() % 1000 - 500) / 500.0  # 0.0 до 1.0 и обратно
                alpha = int(150 + 105 * pulse)  # Альфа канал пульсирует
    
                # Создаем полупрозрачный фон для лучшей читаемости
                background = pygame.Surface((death_rect.width + 40, death_rect.height + respawn_rect.height + 50), pygame.SRCALPHA)
                background.fill((0, 0, 0, alpha))  # Черный с прозрачностью
    
                # Позиционируем фон
                bg_rect = background.get_rect(center=(screen_width // 2, screen_height // 2))
    
                # Отрисовываем все элементы
                screen.blit(background, bg_rect)
                screen.blit(death_text, death_rect)
                screen.blit(respawn_text, respawn_rect)
            
                
        except Exception as e:
            print(f"❌ HUD error: {e}")
            # Минимальный HUD при ошибках
            error_text = self.font.render("HUD ERROR", True, (255, 0, 0))
            screen.blit(error_text, (10, 10))
    
    def draw_hearts(self, screen, current_health, max_health):
        """Отрисовка системы сердец"""
        hearts_count = 3  # 3 сердца
        health_per_heart = 20  # Каждое сердце = 20 HP
        
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