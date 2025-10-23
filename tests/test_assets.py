import unittest
import sys
import os
import pygame

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from game.asset_loader import asset_loader

class TestAssets(unittest.TestCase):
    def setUp(self):
        pygame.init()
    
    def tearDown(self):
        pygame.quit()
    
    def test_asset_loader_initialization(self):
        """Тест инициализации загрузчика ресурсов"""
        self.assertIsNotNone(asset_loader)
        self.assertIsInstance(asset_loader.assets, dict)
        print(f"Asset base path: {asset_loader.base_path}")
    
    def test_player_sprite_loading(self):
        """Тест загрузки спрайта игрока"""
        sprite = asset_loader.load_image("player/alienPink_stand.png", 2)
        self.assertIsNotNone(sprite, "Player sprite should not be None")
        
        if sprite:
            print(f"Player sprite size: {sprite.get_size()}")
            self.assertGreater(sprite.get_width(), 0, "Sprite should have width > 0")
            self.assertGreater(sprite.get_height(), 0, "Sprite should have height > 0")
    
    def test_asset_paths(self):
        """Тест существования файлов ресурсов"""
        assets_to_check = [
            "player/alienPink_stand.png"
        ]
        
        for asset in assets_to_check:
            full_path = os.path.join(asset_loader.base_path, asset)
            exists = os.path.exists(full_path)
            print(f"{asset}: {'✅' if exists else '❌'} {full_path}")
            self.assertTrue(exists, f"Asset file should exist: {asset}")

if __name__ == '__main__':
    unittest.main()