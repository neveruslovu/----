import pygame

class HUD:
    def __init__(self, player):
        self.player = player
        self.font = pygame.font.Font(None, 24)
        
    def update(self, dt):
        pass
    
    def draw(self, screen):
        """Отрисовка HUD"""
        try:
            # Отрисовка здоровья (с проверкой наличия атрибута)
            if hasattr(self.player, 'health_component'):
                health_percent = self.player.health_component.current_health / self.player.health_component.max_health
                health_width = 200 * health_percent
                pygame.draw.rect(screen, (255, 0, 0), (10, 10, health_width, 20))
                health_text = self.font.render(f"Health: {self.player.health_component.current_health}/{self.player.health_component.max_health}", True, (255, 255, 255))
                screen.blit(health_text, (220, 10))
            else:
                # Заглушка если health_component нет
                health_text = self.font.render("Health: 100/100", True, (255, 255, 255))
                screen.blit(health_text, (10, 10))
        
            # Отрисовка уровня (с проверкой наличия атрибута)
            if hasattr(self.player, 'experience') and hasattr(self.player.experience, 'current_level'):
                level_text = f"Level: {self.player.experience.current_level}"
                level_surface = self.font.render(level_text, True, (255, 255, 255))
                screen.blit(level_surface, (10, 40))
            else:
                # Заглушка если experience нет
                level_text = self.font.render("Level: 1", True, (255, 255, 255))
                screen.blit(level_text, (10, 40))
            
        except Exception as e:
            print(f"HUD draw error: {e}")
            # Минимальный HUD при ошибках
            error_text = self.font.render("HUD", True, (255, 255, 255))
            screen.blit(error_text, (10, 10))