import pygame
from .asset_loader import asset_loader

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        
        # Пытаемся загрузить спрайт платформы
        try:
            self.image = asset_loader.load_image("tiles/tile_0000.png", scale=2)
            # Масштабируем под нужный размер
            self.image = pygame.transform.scale(self.image, (width, height))
            print("✅ Загружены спрайты платформ")
        except:
            # Заглушка если нет спрайта
            self.image = pygame.Surface((width, height))
            self.image.fill((100, 100, 100))
            print("🔄 Использую заглушки для платформ")
        
        self.rect = self.image.get_rect(topleft=(x, y))
    
    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self.rect))