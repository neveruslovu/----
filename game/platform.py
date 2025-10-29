# game/platform.py
import pygame
from .asset_loader import asset_loader

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, platform_type="grass", is_trap=False, is_door=False):
        super().__init__()
        
        self.platform_type = platform_type
        self.is_trap = is_trap
        self.is_door = is_door
        
        # 🔥 ИСПОЛЬЗУЕМ TILESET ДЛЯ ПОЛУЧЕНИЯ ИЗОБРАЖЕНИЯ
        self.image = self.get_tile_image(platform_type)
        if self.image:
            self.image = pygame.transform.scale(self.image, (width, height))
        else:
            # Заглушка если тайл не найден
            self.image = pygame.Surface((width, height))
            self.image.fill((100, 200, 100))  # Зеленый для платформ
        
        self.rect = self.image.get_rect(topleft=(x, y))
        self.has_collision = True  # Платформы всегда имеют коллизии
    
    def get_tile_image(self, platform_type):
        """🔥 ПОЛУЧАЕМ ТАЙЛ ИЗ TILESET ПО ТИПУ"""
        # Здесь нужно создать mapping между типами платформ и GID
        type_to_gid = {
            "grass1": 1,  
            "grass_half": 2,
            "grass_half_left": 3,
            "grass_half_mid": 4,
            "grass_half_right": 5,
            "grass_hill_right": 6,
            "grass_round": 7,
            "triangle": 25,
            "semitype1": 57,
            "semitype2": 49, 
            "semitype3": 41,
            "grass2": 9,
            "grass3": 89, 
            "grass4": 97,
            "grass5": 73,
            "grass6": 17,
            "box": 341
        }
        
        gid = type_to_gid.get(platform_type, 1)
        return asset_loader.get_tile_image(gid)
    
    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self.rect))