"""Mock-объекты для тестирования"""
import pygame

class MockImage:
    """Mock для изображения"""
    def __init__(self, width=50, height=50):
        self.width = width
        self.height = height
        self.get_width = lambda: width
        self.get_height = lambda: height

class MockAssetLoader:
    """Mock для загрузки ресурсов"""
    def load_image(self, name, scale=1):
        return MockImage()

class MockCamera:
    """Mock для камеры"""
    def __init__(self):
        self.x = 0
        self.y = 0
        self.offset = pygame.math.Vector2(0, 0)
    
    def update(self, target=None):
        pass

class MockLevel:
    """Mock для уровня"""
    def __init__(self):
        self.platforms = []
        self.enemies = []
        self.background = None
    
    def __len__(self):
        return len(self.platforms) + len(self.enemies)
    
    def draw(self, screen, camera):
        pass
    
    def update(self, dt):
        pass