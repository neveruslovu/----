# game/items/item.py
import pygame
from ..asset_loader import asset_loader

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, item_type):
        super().__init__()
        self.item_type = item_type  # "coin", "key_yellow", "jewel_blue"
        self.rect = pygame.Rect(x, y, width, height)
        self.collected = False
        
        # Загрузка спрайта
        try:
            if item_type == "coin":
                self.image = asset_loader.load_image("Hud/hudCoin.png", scale=1)
            elif item_type == "key_yellow":
                self.image = asset_loader.load_image("Hud/hudKey_yellow.png", scale=1)
            elif item_type == "jewel_blue":
                self.image = asset_loader.load_image("Hud/hudJewel_blue.png", scale=1)
            else:
                self.image = asset_loader.load_image("tiles/boxItem.png", scale=1)
            
            self.image = pygame.transform.scale(self.image, (width, height))
        except:
            # Заглушки
            self.image = pygame.Surface((width, height))
            if item_type == "coin":
                self.image.fill((255, 255, 0))
            elif item_type == "key_yellow":
                self.image.fill((255, 255, 0))
            elif item_type == "jewel_blue":
                self.image.fill((0, 0, 255))
            else:
                self.image.fill((150, 75, 0))
    
    def collect(self):
        """Собирает предмет и возвращает его тип"""
        if not self.collected:
            self.collected = True
            return self.item_type
        return None
    
    def draw(self, screen, camera):
        """Отрисовка предмета"""
        if not self.collected:
            screen.blit(self.image, camera.apply(self.rect))