import pygame
from .asset_loader import asset_loader

# platform.py
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, platform_type="grass", is_trap=False, is_door=False):
        super().__init__()
        
        self.platform_type = platform_type
        self.is_trap = is_trap
        self.is_door = is_door
        
        # 🔥 ДОБАВЛЯЕМ ФИЗИЧЕСКИЕ СВОЙСТВА
        self.has_collision = True  # По умолчанию все платформы имеют коллизии
        
        # Определяем какие типы НЕ должны иметь коллизии
        non_collision_types = ["box", "lock_yellow", "mushroom", "cactus", "bush", "signExit"]
        if platform_type in non_collision_types:
            self.has_collision = False
        
        # Двери и ловушки тоже должны иметь коллизии
        if is_trap or is_door:
            self.has_collision = True
        
        sprite_paths = {
            # platforms
            "grass": "ground/Grass/grass.png",
            "grass_half": "ground/Grass/grassHalf.png",
            "grass_half_left": "ground/Grass/grassHalf_left.png",
            "grass_half_mid": "ground/Grass/grassHalf_mid.png",
            "grass_half_right": "ground/Grass/grassHalf_right.png",
            "grass_hill_right": "ground/Grass/grassHill_right.png",
            "grass_round": "ground/Grass/grassCenter_round.png",
            "box": "tiles/boxItem.png",
            "door_top": "tiles/doorClosed_top.png",
            "door_mid": "tiles/doorClosed_mid.png",
            "doorOpen_mid": "tiles/doorOpen_mid.png",
            "doorOpen_top": "tiles/doorOpen_top.png",
        }
        
        self.image = None
        sprite_path = sprite_paths.get(platform_type, "grass")      
        self.image = asset_loader.load_image(sprite_path, scale=1)
        self.image = pygame.transform.scale(self.image, (width, height))
              
        self.rect = self.image.get_rect(topleft=(x, y))
    
    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self.rect))