# game/asset_loader.py
import pygame
import os

class AssetLoader:
    def __init__(self):
        self.assets = {}
        self.base_path = os.path.join(os.path.dirname(__file__), "assets")
        print(f"🔄 AssetLoader base path: {self.base_path}")  # Добавьте для отладки
    
    def load_image(self, name, scale=1):
        if name in self.assets:
            return self.assets[name]
        
        path = os.path.join(self.base_path, name)
        print(f"🔄 Loading image: {path}")  # Добавьте для отладки
        
        try:
            image = pygame.image.load(path).convert_alpha()
            if scale != 1:
                new_size = (int(image.get_width() * scale), int(image.get_height() * scale))
                image = pygame.transform.scale(image, new_size)
            self.assets[name] = image
            print(f"✅ Successfully loaded: {name}")
            return image
        except pygame.error as e:
            print(f"❌ Failed to load image: {path}")
            print(f"❌ Error: {e}")
            # Создаем заглушку
            stub_surface = pygame.Surface((50, 50), pygame.SRCALPHA)
            pygame.draw.rect(stub_surface, (255, 0, 255), (0, 0, 50, 50))  # Фиолетовый квадрат
            return stub_surface

asset_loader = AssetLoader()