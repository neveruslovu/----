# game/decorations/decoration.py
import pygame
from .asset_loader import asset_loader

class Decoration(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, decoration_type):
        super().__init__()
        self.decoration_type = decoration_type  # "mushroom", "cactus", "bush"
        self.rect = pygame.Rect(x, y, width, height)
        
        # Загрузка спрайта
        try:
            if decoration_type == "mushroom":
                self.image = asset_loader.load_image("tiles/mushroomRed.png", scale=1)
            elif decoration_type == "cactus":
                self.image = asset_loader.load_image("tiles/cactus.png", scale=1)
            elif decoration_type == "bush":
                self.image = asset_loader.load_image("tiles/bush.png", scale=1)
            elif decoration_type == "signExit":
                self.image = asset_loader.load_image("tiles/signExit.png", scale=1)
            else:
                self.image = asset_loader.load_image("tiles/boxItem.png", scale=1)
            
            self.image = pygame.transform.scale(self.image, (width, height))
        except Exception as e:
            print(f"❌ Ошибка загрузки декорации {decoration_type}: {e}")
            # Заглушки
            self.image = pygame.Surface((width, height))
            if decoration_type == "mushroom":
                self.image.fill((255, 100, 100))
            elif decoration_type == "cactus":
                self.image.fill((100, 200, 100))
            elif decoration_type == "bush":
                self.image.fill((50, 150, 50))
            else:
                self.image.fill((150, 75, 0))
    
    def draw(self, screen, camera):
        """Отрисовка декорации"""
        screen.blit(self.image, camera.apply(self.rect))