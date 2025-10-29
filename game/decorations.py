# game/decorations.py
import pygame
from .asset_loader import asset_loader

class Decoration(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, decoration_type):
        super().__init__()
        
        self.decoration_type = decoration_type
        self.has_collision = False  # 🔥 ДЕКОРАЦИИ НЕ ИМЕЮТ КОЛЛИЗИЙ
        
        # 🔥 ИСПОЛЬЗУЕМ TILESET ДЛЯ ПОЛУЧЕНИЯ ИЗОБРАЖЕНИЯ
        self.image = self.get_tile_image(decoration_type)
        if self.image:
            self.image = pygame.transform.scale(self.image, (width, height))
        else:
            # Заглушка если тайл не найден
            self.image = pygame.Surface((width, height))
            if decoration_type == "mushroom":
                self.image.fill((255, 100, 100))
            elif decoration_type == "cactus":
                self.image.fill((0, 200, 0))
            else:
                self.image.fill((150, 150, 150))
        
        self.rect = self.image.get_rect(topleft=(x, y))
    
    def get_tile_image(self, decoration_type):
        """🔥 ПОЛУЧАЕМ ТАЙЛ ИЗ TILESET ПО ТИПУ"""
        type_to_gid = {
            "dec1": 347,
            "dec2": 356, 
            "dec3": 364,
            "dec4": 372,       
            "dec5": 380,
            "dec6": 349,
            "lock_yellow":363
        }
        
        gid = type_to_gid.get(decoration_type, 341)  # По умолчанию box
        return asset_loader.get_tile_image(gid)
    
    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self.rect))