# game/assets.py
import pygame
import os

class AssetLoader:
    def __init__(self):
        self.assets = {}
        self.base_path = os.path.join(os.path.dirname(__file__), "assets")
    
    def load_image(self, name, scale=1):
        if name in self.assets:
            return self.assets[name]
        
        path = os.path.join(self.base_path, name)
        try:
            image = pygame.image.load(path).convert_alpha()
            if scale != 1:
                new_size = (int(image.get_width() * scale), int(image.get_height() * scale))
                image = pygame.transform.scale(image, new_size)
            self.assets[name] = image
            return image
        except pygame.error as e:
            print(f"Не удалось загрузить изображение: {path}")
            print(e)
            return None

# Создаем глобальный экземпляр
asset_loader = AssetLoader()