import pygame

class HUD:
    def __init__(self, player):
        self.player = player
        self.font = pygame.font.Font(None, 24)
        
    def update(self, dt):
        pass
    
    def draw(self, screen):
        # Полоска здоровья
        health_percent = self.player.health_component.current_health / self.player.health_component.max_health
        health_width = 200
        health_rect = pygame.Rect(10, 10, health_width, 20)
        current_health_rect = pygame.Rect(10, 10, health_width * health_percent, 20)
        
        pygame.draw.rect(screen, (255, 0, 0), health_rect)
        pygame.draw.rect(screen, (0, 255, 0), current_health_rect)
        pygame.draw.rect(screen, (255, 255, 255), health_rect, 2)
        
        # Текст здоровья
        health_text = f"HP: {self.player.health_component.current_health}/{self.player.health_component.max_health}"
        text_surface = self.font.render(health_text, True, (255, 255, 255))
        screen.blit(text_surface, (15, 12))
        
        # Уровень
        level_text = f"Level: {self.player.experience.current_level}"
        screen.blit(self.font.render(level_text, True, (255, 255, 255)), (10, 40))