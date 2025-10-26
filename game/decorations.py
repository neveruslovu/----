# game/decorations/decoration.py
import pygame
from .asset_loader import asset_loader

# decorations.py (если у вас есть этот файл)
class Decoration(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, decoration_type):
        super().__init__()
        
        self.decoration_type = decoration_type
        self.has_collision = False  # 🔥 ДЕКОРАЦИИ НЕ ИМЕЮТ КОЛЛИЗИЙ
        
        # Загрузка спрайта для декорации
        try:
            sprite_paths = {
                "mushroom": "tiles/mushroomRed.png",
                "cactus": "tiles/cactus.png", 
                "bush": "tiles/bush.png",
                "signExit": "tiles/signExit.png",
                "box": "tiles/boxItem.png",
                "lock_yellow": "tiles/lock_yellow.png"
            }
            
            path = sprite_paths.get(decoration_type, "tiles/boxItem.png")
            self.image = asset_loader.load_image(path, scale=1)
            self.image = pygame.transform.scale(self.image, (width, height))
            
        except Exception as e:
            print(f"❌ Ошибка загрузки декорации {decoration_type}: {e}")
            # Заглушка
            self.image = pygame.Surface((width, height))
            if decoration_type == "mushroom":
                self.image.fill((255, 100, 100))
            elif decoration_type == "cactus":
                self.image.fill((0, 200, 0))
            else:
                self.image.fill((150, 150, 150))
        
        self.rect = self.image.get_rect(topleft=(x, y))
    
    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self.rect))